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
from collections import Counter
from collections import defaultdict
from prometheus_client import CollectorRegistry, generate_latest, Gauge, CONTENT_TYPE_LATEST
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)

class CinderServiceStats(OSBase):
    """ Class to report the statistics on Cinder services.

        state of workers broken down by state
    """
    def build_cache_data(self):

        aggregated_workers = defaultdict(Counter)

        stats = self.osclient.get_workers('cinder')
        for worker in stats:
            service = worker['service']
            state = worker['state']
            aggregated_workers[service][state] += 1

        for service in aggregated_workers:
            totalw = sum(aggregated_workers[service].values())
            for state in self.osclient.states:
                prct = (100.0 * aggregated_workers[service][state]) / totalw
                stats.append({
                    'stat_name': "services_{}_{}_percent".format(service, state),
                    'stat_value': prct,
                    'state': state,
                    'service': service
                })
                stats.append({
                    'stat_name': "services_{}_{}_total".format(service, state),
                    'stat_value': aggregated_workers[service][state],
                    'state': state,
                    'service': service
                })

        return stats

    def get_cache_key(self):
        return "cinder_services_stats"

    def get_stats(self):
        registry = CollectorRegistry()
        labels = ['region', 'host', 'service', 'state']
        cinder_services_stats_cache = self.get_cache_data()
        for cinder_services_stat in cinder_services_stats_cache:
            stat_gauge = Gauge(self.gauge_name_sanitize(cinder_services_stat['stat_name']),
                         'Openstack Cinder Service statistic',
                         labels, registry=registry)
            label_values = [self.osclient.region,
                            cinder_services_stat.get('host', ''),
                            cinder_services_stat.get('service', ''),
                            cinder_services_stat.get('state', '')]
            stat_gauge.labels(*label_values).set(cinder_services_stat['stat_value'])
        return generate_latest(registry)
