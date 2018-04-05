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

from base import OSBase

from urlparse import urlparse
from prometheus_client import CollectorRegistry, generate_latest, Gauge
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)


class CheckOSApi(OSBase):
    """Class to check the status of OpenStack API services."""

    CHECK_MAP = {
        'keystone': {'path': '/', 'expect': [300], 'name': 'keystone-public-api'},
        'heat': {'path': '/', 'expect': [300], 'name': 'heat-api'},
        'heat-cfn': {'path': '/', 'expect': [300], 'name': 'heat-cfn-api'},
        'glance': {'path': '/', 'expect': [300], 'name': 'glance-api'},
        'cinder': {'path': '/', 'expect': [200, 300], 'name': 'cinder-api'},
        'cinderv2': {
            'path': '/', 'expect': [200, 300], 'name': 'cinder-v2-api'},
        'neutron': {'path': '/', 'expect': [200], 'name': 'neutron-api'},
        'nova': {'path': '/', 'expect': [200], 'name': 'nova-api'},
        'ceilometer': {
            'path': 'v2/capabilities', 'expect': [200], 'auth': True,
            'name': 'ceilometer-api'},
        'swift': {'path': '/', 'expect': [200], 'name': 'ceph'},
        'swift_s3': {
            'path': 'healthcheck', 'expect': [200], 'name': 'swift-s3-api'},
        'murano': {'path': '/', 'expect': [200, 300], 'name': 'murano-api'},
        'trove': {'path': '/', 'expect': [200, 300], 'name': 'trove-api'},
        'mistral': {'path': '/', 'expect': [200, 300], 'name': 'mistral-api'},
        'designate': {'path': '/', 'expect': [200, 300], 'name': 'designate-api'},
        'contrail_analytics': {'path': '/', 'expect': [200], 'name': 'contrail-analytics-api'},
        'contrail_config': {'path': '/', 'expect': [200], 'name': 'contrail-config-api'},
        'congress': {'path': '/', 'expect': [200], 'name': 'congress-api'},
        'placement': {'path': '/', 'expect': [401], 'name': 'placement-api'},
    }

    def _service_url(self, endpoint, path):
        url = urlparse(endpoint)
        u = '%s://%s' % (url.scheme, url.netloc)
        if path != '/':
            u = '%s/%s' % (u, path)
        return u

    def build_cache_data(self):
        """ Check the status of all the API services.

            Yields a list of dict items with 'service', 'status' (either OK,
            FAIL or UNKNOWN) and 'region' keys.
        """
        check_array = []
        catalog = self.osclient.service_catalog

        for service in catalog:
            name = service['name']
            url = None
            status_code = 500
            if name not in self.CHECK_MAP:
                logger.info(
                    "No check found for service '%s', creating one" % name)
                self.CHECK_MAP[name] = {
                    'path': '/',
                    'expect': [200, 300, 302, 401, 404],
                    'name': name,
                }
            check = self.CHECK_MAP[name]
            url = self._service_url(service['url'], check['path'])
            r = self.osclient.raw_get(
                url, token_required=check.get(
                    'auth', False))

            if r is not None:
                status_code = r.status_code

            if r is None or status_code not in check['expect']:
                logger.info(
                    "Service %s check failed "
                    "(returned '%s' but expected '%s')" % (
                        name, status_code, check['expect'])
                )
                status = self.FAIL
            else:
                status = self.OK

            check_array.append({
                'service': name,
                'status': status,
                'url': url,
                'status_code': status_code,
                'region': self.osclient.region,
            })
        return check_array

    def get_cache_key(self):
        return "check_os_api"

    def get_stats(self):
        registry = CollectorRegistry()
        labels = ['region', 'url', 'service']
        check_api_data_cache = self.get_cache_data()
        for check_api_data in check_api_data_cache:
            label_values = [
                check_api_data['region'],
                check_api_data['url'],
                check_api_data['service']]
            gague_name = self.gauge_name_sanitize(
                "check_{}_api".format(check_api_data['service']))
            check_gauge = Gauge(
                gague_name,
                'Openstack API check. fail = 0, ok = 1 and unknown = 2',
                labels,
                registry=registry)
            check_gauge.labels(*label_values).set(check_api_data['status'])
        return generate_latest(registry)
