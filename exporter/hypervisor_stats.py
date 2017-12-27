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

from prometheus_client import CollectorRegistry, generate_latest, Gauge, CONTENT_TYPE_LATEST
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)

class HypervisorStats(OSBase):
    """ Class to report the statistics on Nova hypervisors."""
    VALUE_MAP = {
        'current_workload': 'running_tasks',
        'running_vms': 'running_instances',
        'local_gb_used': 'used_disk_GB',
        'free_disk_gb': 'free_disk_GB',
        'memory_mb_used': 'used_ram_MB',
        'free_ram_mb': 'free_ram_MB',
        'vcpus_used': 'used_vcpus',
    }

    def __init__(self, oscache, osclient, cpu_overcommit_ratio, ram_overcommit_ratio):
        super(HypervisorStats, self).__init__(oscache, osclient)
        self.cpu_overcommit_ratio = cpu_overcommit_ratio
        self.ram_overcommit_ratio = ram_overcommit_ratio

    def build_cache_data(self):
        cache_stats = []
        nova_aggregates = {}
        r = self.osclient.get('nova', 'os-aggregates')
        if not r:
            logger.warning("Could not get nova aggregates")
        else:
            aggregates_list = r.json().get('aggregates', [])
            for agg in aggregates_list:
                nova_aggregates[agg['name']] = {
                    'id': agg['id'],
                    'hosts': [h.split('.')[0] for h in agg['hosts']],
                    'metrics': {'free_vcpus': 0},
                }
                nova_aggregates[agg['name']]['metrics'].update(
                    {v: 0 for v in self.VALUE_MAP.values()}
                )

        r = self.osclient.get('nova', 'os-hypervisors/detail')
        if not r:
            logger.warning("Could not get hypervisor statistics")
            return

        total_stats = {v: 0 for v in self.VALUE_MAP.values()}
        total_stats['free_vcpus'] = 0
        hypervisor_stats = r.json().get('hypervisors', [])
        for stats in hypervisor_stats:
            host = stats['hypervisor_hostname']
            for k, v in self.VALUE_MAP.iteritems():
                m_val = stats.get(k, 0)
                cache_stats.append({
                    'stat_name': v,
                    'stat_value': m_val,
                    'host': host,
                })
                total_stats[v] += m_val
                for agg in nova_aggregates.keys():
                    agg_hosts = nova_aggregates[agg]['hosts']
                    if host in agg_hosts:
                        nova_aggregates[agg]['metrics'][v] += m_val
            m_vcpus = stats.get('vcpus', 0)
            m_vcpus_used = stats.get('vcpus_used', 0)
            free = (int(self.cpu_overcommit_ratio * m_vcpus)) - m_vcpus_used
            cache_stats.append({
                'stat_name': 'free_vcpus',
                'stat_value': free,
                'host': host,
            })
            total_stats['free_vcpus'] += free
            for agg in nova_aggregates.keys():
                agg_hosts = nova_aggregates[agg]['hosts']
                if host in agg_hosts:
                    free = ((int(self.extra_config['cpu_ratio'] *
                                 m_vcpus)) -
                            m_vcpus_used)
                    nova_aggregates[agg]['metrics']['free_vcpus'] += free

        # Dispatch the aggregate metrics
        for agg in nova_aggregates.keys():
            agg_id = nova_aggregates[agg]['id']
            agg_total_free_ram = (
                nova_aggregates[agg]['metrics']['free_ram_MB'] +
                nova_aggregates[agg]['metrics']['used_ram_MB']
            )
            if agg_total_free_ram > 0:
                nova_aggregates[agg]['metrics']['free_ram_percent'] = round(
                    (100.0 * nova_aggregates[agg]['metrics']['free_ram_MB']) /
                    agg_total_free_ram,
                    2)
            for k, v in nova_aggregates[agg]['metrics'].iteritems():
                cache_stats.append({
                    'stat_name': 'aggregate_{}'.format(k),
                    'stat_value': v,
                    'aggregate': agg,
                    'aggregate_id': agg_id,
                })
        # Dispatch the global metrics
        for k, v in total_stats.iteritems():
            cache_stats.append({
                'stat_name': 'total_{}'.format(k),
                'stat_value': v,
            })

        return cache_stats

    def get_cache_key(self):
        return "hypervisor_stats"

    def get_stats(self):
        registry = CollectorRegistry()
        labels = ['region', 'host', 'aggregate', 'aggregate_id']
        hypervisor_stats_cache = self.get_cache_data()
        for hypervisor_stat in hypervisor_stats_cache:
            stat_gauge = Gauge(self.gauge_name_sanitize(hypervisor_stat['stat_name']),
                         'Openstack Hypervisor statistic',
                         labels, registry=registry)
            label_values = [self.osclient.region,
                            hypervisor_stat.get('host', ''),
                            hypervisor_stat.get('aggregate', ''),
                            hypervisor_stat.get('aggregate_id', '')]
            stat_gauge.labels(*label_values).set(hypervisor_stat['stat_value'])
        return generate_latest(registry)
