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

import argparse
import yaml
import os
import traceback
import urlparse
from threading import Thread
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from SocketServer import ForkingMixIn
from prometheus_client import CONTENT_TYPE_LATEST

from osclient import OSClient
from oscache import OSCache
from check_os_api import CheckOSApi
from neutron_agents import NeutronAgentStats
from nova_services import NovaServiceStats
from cinder_services import CinderServiceStats
from hypervisor_stats import HypervisorStats

import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)

collectors = []

class ForkingHTTPServer(ForkingMixIn, HTTPServer):
    pass

class OpenstackExporterHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def do_GET(self):
        url = urlparse.urlparse(self.path)
        if url.path == '/metrics':
            output = ''
            try:
                for collector in collectors:
                    stats = collector.get_stats()
                    if stats is not None:
                        output = output + stats
                self.send_response(200)
                self.send_header('Content-Type', CONTENT_TYPE_LATEST)
                self.end_headers()
                self.wfile.write(output)
            except:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(traceback.format_exc())
        elif url.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write("""<html>
            <head><title>OpenStack Exporter</title></head>
            <body>
            <h1>OpenStack Exporter</h1>
            <p>Visit <code>/metrics</code> to use.</p>
            </body>
            </html>""")
        else:
            self.send_response(404)
            self.end_headers()


def handler(*args, **kwargs):
    OpenstackExporterHandler(*args, **kwargs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage=__doc__,
                                     description='Prometheus OpenStack exporter',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--config-file', nargs='?',
                        help='Configuration file path',
                        type=argparse.FileType('r'),
                        required=False)
    args = parser.parse_args()
    config = {}
    if args.config_file:
        config = yaml.safe_load(args.config_file.read())

    os_keystone_url = config.get('OS_AUTH_URL', os.getenv('OS_AUTH_URL'))
    os_password = config.get('OS_PASSWORD', os.getenv('OS_PASSWORD'))
    os_tenant_name = config.get('OS_PROJECT_NAME', os.getenv('OS_PROJECT_NAME'))
    os_username = config.get('OS_USERNAME', os.getenv('OS_USERNAME'))
    os_user_domain = config.get('OS_USER_DOMAIN_NAME', os.getenv('OS_USER_DOMAIN_NAME'))
    os_region = config.get('OS_REGION_NAME', os.getenv('OS_REGION_NAME'))
    os_timeout = config.get('TIMEOUT_SECONDS', int(os.getenv('TIMEOUT_SECONDS', 10)))
    os_polling_interval = config.get('OS_POLLING_INTERVAL', int(os.getenv('OS_POLLING_INTERVAL', 900)))
    os_retries = config.get('OS_RETRIES', int(os.getenv('OS_RETRIES', 1)))
    os_cpu_overcomit_ratio = config.get('OS_CPU_OC_RATIO', float(os.getenv('OS_CPU_OC_RATIO', 1)))
    os_ram_overcomit_ratio = config.get('OS_RAM_OC_RATIO', float(os.getenv('OS_RAM_OC_RATIO', 1)))

    osclient = OSClient(os_keystone_url, os_password, os_tenant_name, os_username, os_user_domain, os_region, os_timeout, os_retries)
    oscache = OSCache(os_polling_interval, os_region)
    collectors.append(oscache)

    check_os_api = CheckOSApi(oscache, osclient)
    collectors.append(check_os_api)
    neutron_agent_stats = NeutronAgentStats(oscache, osclient)
    collectors.append(neutron_agent_stats)
    cinder_service_stats = CinderServiceStats(oscache, osclient)
    collectors.append(cinder_service_stats)
    nova_service_stats = NovaServiceStats(oscache, osclient)
    collectors.append(nova_service_stats)
    hypervisor_stats = HypervisorStats(oscache, osclient, os_cpu_overcomit_ratio, os_ram_overcomit_ratio)
    collectors.append(hypervisor_stats)

    oscache.start()

    listen_port = config.get('LISTEN_PORT', int(os.getenv('LISTEN_PORT', 19103)))
    server = ForkingHTTPServer(('', listen_port), handler)
    server.serve_forever()
