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

from base import OSBase, OSCollector
from collections import Counter
from collections import defaultdict
from prometheus_client import CollectorRegistry, generate_latest
from prometheus_client.core import GaugeMetricFamily
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)


class NovaServiceStats(OSBase):
    """ Class to report the statistics on Nova services.

        status per service broken down by state
    """

    def build_cache_data(self):
        # Get information of the state per service
        # State can be: 'up', 'down' or 'disabled'
        aggregated_workers = defaultdict(Counter)
        stats = self.osclient.get_workers('nova')
        for worker in stats:
            service = worker['service']
            state = worker['state']
            aggregated_workers[service][state] += 1

        for service in aggregated_workers:
            total = sum(aggregated_workers[service].values())
            for state in self.osclient.states:
                prct = 0
                if total > 0:
                    prct = (100.0 * aggregated_workers[service][state]) / total

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
        return "nova_services_stats"

    def get_stats(self):
        registry = CollectorRegistry()
        labels = ['region', 'host', 'service', 'state']
        services_stats_cache = self.get_cache_data()
        services_stats_cache.sort(key=self.take_stat_name)
        REGISTRY_FLAG = ''
        stat_gauge = []

        for services_stat in services_stats_cache:
            label_values = [self.osclient.region,
                            services_stat.get('host', ''),
                            services_stat.get('service', ''),
                            services_stat.get('state', '')]
            if REGISTRY_FLAG != services_stat['stat_name']:
                if REGISTRY_FLAG:
                    registry.register(OSCollector(stat_gauge))
                stat_gauge = GaugeMetricFamily(
                    self.gauge_name_sanitize(
                        services_stat['stat_name']),
                    'Openstack Nova Service statistic',
                    labels=labels)
                REGISTRY_FLAG = services_stat['stat_name']

            stat_gauge.add_metric(label_values,
                                  services_stat['stat_value'])
        registry.register(OSCollector(stat_gauge))
        return generate_latest(registry)
