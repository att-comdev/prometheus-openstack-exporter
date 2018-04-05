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
from prometheus_client import CollectorRegistry, generate_latest, Gauge
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)


class NeutronAgentStats(OSBase):
    """ Class to report the statistics on Neutron agents.

        state of agents
    """

    def build_cache_data(self):

        # Get information of the state per agent
        # State can be up or down
        aggregated_agents = defaultdict(Counter)
        stats = self.osclient.get_workers('neutron')

        for agent in stats:
            service = agent['service']
            state = agent['state']
            aggregated_agents[service][state] += 1

        for service in aggregated_agents:
            totala = sum(aggregated_agents[service].values())
            for state in self.osclient.states:
                prct = (100.0 * aggregated_agents[service][state]) / totala
                stats.append({
                    'stat_name': "services_{}_{}_percent".format(service, state),
                    'stat_value': prct,
                    'service': service,
                    'state': state
                })
                stats.append({
                    'stat_name': "services_{}_{}_total".format(service, state),
                    'stat_value': aggregated_agents[service][state],
                    'service': service,
                    'state': state,
                })
        return stats

    def get_cache_key(self):
        return "neutron_agent_stats"

    def get_stats(self):
        registry = CollectorRegistry()
        labels = ['region', 'host', 'service', 'state']
        neutron_agent_stats_cache = self.get_cache_data()
        for neutron_agent_stat in neutron_agent_stats_cache:
            stat_gauge = Gauge(
                self.gauge_name_sanitize(
                    neutron_agent_stat['stat_name']),
                'Openstack Neutron agent statistic',
                labels,
                registry=registry)
            label_values = [self.osclient.region,
                            neutron_agent_stat.get('host', ''),
                            neutron_agent_stat.get('service', ''),
                            neutron_agent_stat.get('state', '')]
            stat_gauge.labels(
                *
                label_values).set(
                neutron_agent_stat['stat_value'])
        return generate_latest(registry)
