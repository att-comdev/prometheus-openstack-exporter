#!/usr/bin/env python
# Copyright 2017 The Openstack-Helm Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import dateutil.parser
import dateutil.tz
import requests
import simplejson as json
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)


class KeystoneException(Exception):
    pass


class OSClient(object):
    """ Base class for querying the OpenStack API endpoints.

    It uses the Keystone service catalog to discover the API endpoints.
    """
    EXPIRATION_TOKEN_DELTA = datetime.timedelta(0, 30)
    states = {'up': 1, 'down': 0, 'disabled': 2}

    def __init__(
            self,
            keystone_url,
            password,
            tenant_name,
            username,
            user_domain,
            region,
            timeout,
            retries):
        self.keystone_url = keystone_url
        self.password = password
        self.tenant_name = tenant_name
        self.username = username
        self.user_domain = user_domain
        self.region = region
        self.timeout = timeout
        self.retries = retries
        self.token = None
        self.valid_until = None
        self.session = requests.Session()
        self.session.mount(
            'http://', requests.adapters.HTTPAdapter(max_retries=retries))
        self.session.mount(
            'https://', requests.adapters.HTTPAdapter(max_retries=retries))
        self._service_catalog = []

    def is_valid_token(self):
        now = datetime.datetime.now(tz=dateutil.tz.tzutc())
        return self.token is not None and self.valid_until is not None and self.valid_until > now

    def clear_token(self):
        self.token = None
        self.valid_until = None

    def get_token(self):
        self.clear_token()
        data = json.dumps({
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "name": self.username,
                            "domain": {"id": self.user_domain},
                            "password": self.password
                        }
                    }
                },
                "scope": {
                    "project": {
                        "name": self.tenant_name,
                        "domain": {"id": self.user_domain}
                    }
                }
            }
        })
        logger.info("Trying to get token from '%s'" % self.keystone_url)
        r = self.make_request('post',
                              '%s/auth/tokens' % self.keystone_url, data=data,
                              token_required=False)
        if not r:
            logger.error(
                "Cannot get a valid token from {}".format(
                    self.keystone_url))

        if r.status_code < 200 or r.status_code > 299:
            logger.error(
                "{} responded with code {}".format(
                    self.keystone_url,
                    r.status_code))

        data = r.json()
        self.token = r.headers.get("X-Subject-Token")
        self.tenant_id = data['token']['project']['id']
        self.valid_until = dateutil.parser.parse(
            data['token']['expires_at']) - self.EXPIRATION_TOKEN_DELTA
        self._service_catalog = []
        for item in data['token']['catalog']:
            internalURL = None
            publicURL = None
            adminURL = None
            for endpoint in item['endpoints']:
                if endpoint['region'] == self.region or self.region is None:
                    if endpoint['interface'] == 'internal':
                        internalURL = endpoint['url']
                    elif endpoint['interface'] == 'public':
                        publicURL = endpoint['url']
                    elif endpoint['interface'] == 'admin':
                        adminURL = endpoint['url']

            if internalURL is None and publicURL is None:
                logger.warning(
                    "Service '{}' skipped because no URL can be found".format(
                        item['name']))
                continue
            self._service_catalog.append({
                'name': item['name'],
                'region': self.region,
                'service_type': item['type'],
                'url': internalURL if internalURL is not None else publicURL,
                'admin_url': adminURL,
            })

        logger.debug("Got token '%s'" % self.token)
        return self.token

    @property
    def service_catalog(self):
        if not self._service_catalog:
            self.get_token()
        return self._service_catalog

    @service_catalog.setter
    def service_catalog(self, service_catalog):
        self._service_catalog = service_catalog

    def get_service(self, service_name):
        return next((x for x in self._service_catalog
                     if x['name'] == service_name), None)

    def raw_get(self, url, token_required=False):
        return self.make_request('get', url,
                                 token_required=token_required)

    def make_request(self, verb, url, data=None, token_required=True,
                     params=None):
        kwargs = {
            'url': url,
            'timeout': self.timeout,
            'headers': {'Content-type': 'application/json'}
        }
        if token_required and not self.is_valid_token():
            self.get_token()
            if not self.is_valid_token():
                logger.error("Aborting request, no valid token")
                return
        if token_required:
            kwargs['headers']['X-Auth-Token'] = self.token

        if data is not None:
            kwargs['data'] = data

        if params is not None:
            kwargs['params'] = params

        func = getattr(self.session, verb.lower())

        try:
            r = func(**kwargs)
        except Exception as e:
            logger.error("Got exception for '%s': '%s'" %
                         (kwargs['url'], e))
            return

        logger.info("%s responded with status code %d" %
                    (kwargs['url'], r.status_code))

        return r

    def get(self, service, resource, params=None):
        url = self._build_url(service, resource)
        if not url:
            return
        logger.info('GET({}) {}'.format(url, params))
        return self.make_request('get', url, params=params)

    def _build_url(self, service, resource):
        s = (self.get_service(service) or {})
        url = s.get('url')
        # v3 API must be used in order to obtain tenants in multi-domain envs
        if service == 'keystone' and (resource in ['projects',
                                                   'users', 'roles']):
            url = url.replace('v2.0', 'v3')

        if url:
            if url[-1] != '/':
                url += '/'
            url = "%s%s" % (url, resource)
        else:
            logger.error("Service '%s' not found in catalog" % service)
        return url

    def get_workers(self, service):
        """ Return the list of workers and their state

        Here is an example of returned dictionnary:
        {
          'host': 'node.example.com',
          'service': 'nova-compute',
          'state': 'up'
        }

        where 'state' can be 'up', 'down' or 'disabled'
        """
        worker_metrics = []
        if service == 'neutron':
            endpoint = 'v2.0/agents'
            entry = 'agents'
        else:
            endpoint = 'os-services'
            entry = 'services'

        ost_services_r = self.get(service, endpoint)

        msg = "Cannot get state of {} workers".format(service)
        if ost_services_r is None:
            logger.warning(msg)
        elif ost_services_r.status_code != 200:
            msg = "{}: Got {} ({})".format(
                msg, ost_services_r.status_code, ost_services_r.content)
            logger.warning(msg)
        else:
            try:
                r_json = ost_services_r.json()
            except ValueError:
                r_json = {}

            if entry not in r_json:
                msg = "{}: couldn't find '{}' key".format(msg, entry)
                logger.warning(msg)
            else:
                for val in r_json[entry]:
                    data = {'host': val['host'], 'service': val['binary']}

                    if service == 'neutron':
                        if not val['admin_state_up']:
                            data['state'] = 'disabled'
                        else:
                            data['state'] = 'up' if val['alive'] else 'down'
                    else:
                        if val['status'] == 'disabled':
                            data['state'] = 'disabled'
                        elif val['state'] == 'up' or val['state'] == 'down':
                            data['state'] = val['state']
                        else:
                            data['state'] = 'unknown'
                            msg = "Unknown state for {} workers:{}".format(
                                service, val['state'])
                            logger.warning(msg)
                            continue
                    data['stat_value'] = self.states[data['state']]
                    data['stat_name'] = "services_{}_{}".format(
                        service, val['binary'])
                    worker_metrics.append(data)
        return worker_metrics
