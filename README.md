Prometheus Openstack Exporter
============

Image for a prometheus exporter for openstack API derived metrics.

## Environment

check sample_env_file provided in the source.

* OS_USERNAME
  - username associated with the monitoring tenant/project in openstack, used for polling openstack API, **required**

* OS_PASSWORD
  - password for the username associated with the monitoring tenant/project in openstack, used for polling openstack API, **required**

* OS_PROJECT_NAME
  - monitoring tenant/project in openstack, used for polling openstack API, **required**

* OS_AUTH_URL
  - openstack keystone API endpoint, **required**

* LISTEN_PORT
  - port to bind for prometheus scrape target

* OS_REGION_NAME
  - openstack region to use keystone service catalog against

* TIMEOUT_SECONDS
  - number of seconds before API calls should timeout

* OS_POLLING_INTERVAL
  - interval in seconds between API polls

* OS_RETRIES
  - number of retries on API calls before failing

* OS_CPU_OC_RATIO
  - CPU overcommit ratio for the hypervisor

* OS_RAM_OC_RATIO=1
  - RAM overcommit ratio for the hypervisor

## Docker Usage

docker run --env-file sample_env_file -it rakeshpatnaik/prometheus-openstack-exporter:v0.1

## sample test
docker exec \<instance-id\> curl http://localhost:19103
```
# HELP openstack_exporter_cache_refresh_duration_seconds Cache refresh duration in seconds.
# TYPE openstack_exporter_cache_refresh_duration_seconds gauge
openstack_exporter_cache_refresh_duration_seconds{region="RegionOne"} 0.12850117683410645
# HELP check_openstack_api Openstack API check fail = 0, ok = 1 and unknown = 3
# TYPE check_openstack_api gauge
check_openstack_api{region="RegionOne",service="congress",status_code="NA",url="None"} 2.0
# HELP check_openstack_api Openstack API check fail = 0, ok = 1 and unknown = 3
# TYPE check_openstack_api gauge
check_openstack_api{region="RegionOne",service="ceph",status_code="200",url="http://ceph-rgw.ceph.svc.cluster.local:8088"} 1.0
# HELP check_openstack_api Openstack API check fail = 0, ok = 1 and unknown = 3
# TYPE check_openstack_api gauge
check_openstack_api{region="RegionOne",service="glance-api",status_code="300",url="http://glance-api.openstack.svc.cluster.local:9292"} 1.0
# HELP check_openstack_api Openstack API check fail = 0, ok = 1 and unknown = 3
# TYPE check_openstack_api gauge
check_openstack_api{region="RegionOne",service="nova-api",status_code="200",url="http://nova-api.openstack.svc.cluster.local:8774"} 1.0
# HELP check_openstack_api Openstack API check fail = 0, ok = 1 and unknown = 3
# TYPE check_openstack_api gauge
check_openstack_api{region="RegionOne",service="heat",status_code="NA",url="None"} 2.0
# HELP check_openstack_api Openstack API check fail = 0, ok = 1 and unknown = 3
# TYPE check_openstack_api gauge
check_openstack_api{region="RegionOne",service="neutron-api",status_code="200",url="http://neutron-server.openstack.svc.cluster.local:9696"} 1.0
# HELP check_openstack_api Openstack API check fail = 0, ok = 1 and unknown = 3
# TYPE check_openstack_api gauge
check_openstack_api{region="RegionOne",service="placement",status_code="NA",url="None"} 2.0
# HELP check_openstack_api Openstack API check fail = 0, ok = 1 and unknown = 3
# TYPE check_openstack_api gauge
check_openstack_api{region="RegionOne",service="heat-cfn-api",status_code="300",url="http://heat-cfn.openstack.svc.cluster.local:8000"} 1.0
# HELP check_openstack_api Openstack API check fail = 0, ok = 1 and unknown = 3
# TYPE check_openstack_api gauge
check_openstack_api{region="RegionOne",service="keystone-public-api",status_code="300",url="http://keystone-api.openstack.svc.cluster.local:80"} 1.0
# HELP neutron_agents_percent Openstack Neutron agent statistic
# TYPE neutron_agents_percent gauge
neutron_agents_percent{host="",region="RegionOne",service="neutron-dhcp-agent",state="disabled"} 0.0
# HELP neutron_agents_percent Openstack Neutron agent statistic
# TYPE neutron_agents_percent gauge
neutron_agents_percent{host="",region="RegionOne",service="neutron-l3-agent",state="up"} 100.0
# HELP neutron_agents Openstack Neutron agent statistic
# TYPE neutron_agents gauge
neutron_agents{host="",region="RegionOne",service="neutron-metadata-agent",state="up"} 1.0
# HELP neutron_agents Openstack Neutron agent statistic
# TYPE neutron_agents gauge
neutron_agents{host="ubuntu-xenial",region="RegionOne",service="neutron-metadata-agent",state="up"} 0.0
# HELP neutron_agents Openstack Neutron agent statistic
# TYPE neutron_agents gauge
neutron_agents{host="",region="RegionOne",service="neutron-metadata-agent",state="down"} 0.0
# HELP neutron_agents Openstack Neutron agent statistic
# TYPE neutron_agents gauge
neutron_agents{host="",region="RegionOne",service="neutron-openvswitch-agent",state="up"} 1.0
# HELP neutron_agents_percent Openstack Neutron agent statistic
# TYPE neutron_agents_percent gauge
neutron_agents_percent{host="",region="RegionOne",service="neutron-openvswitch-agent",state="disabled"} 0.0
# HELP neutron_agents_percent Openstack Neutron agent statistic
# TYPE neutron_agents_percent gauge
neutron_agents_percent{host="",region="RegionOne",service="neutron-openvswitch-agent",state="down"} 0.0
# HELP neutron_agents Openstack Neutron agent statistic
# TYPE neutron_agents gauge
neutron_agents{host="ubuntu-xenial",region="RegionOne",service="neutron-l3-agent",state="up"} 0.0
# HELP neutron_agents_percent Openstack Neutron agent statistic
# TYPE neutron_agents_percent gauge
neutron_agents_percent{host="",region="RegionOne",service="neutron-metadata-agent",state="disabled"} 0.0
# HELP neutron_agents Openstack Neutron agent statistic
# TYPE neutron_agents gauge
neutron_agents{host="ubuntu-xenial",region="RegionOne",service="neutron-dhcp-agent",state="up"} 0.0
# HELP neutron_agents_percent Openstack Neutron agent statistic
# TYPE neutron_agents_percent gauge
neutron_agents_percent{host="",region="RegionOne",service="neutron-dhcp-agent",state="up"} 100.0
# HELP neutron_agents_percent Openstack Neutron agent statistic
# TYPE neutron_agents_percent gauge
neutron_agents_percent{host="",region="RegionOne",service="neutron-l3-agent",state="down"} 0.0
# HELP neutron_agents Openstack Neutron agent statistic
# TYPE neutron_agents gauge
neutron_agents{host="",region="RegionOne",service="neutron-openvswitch-agent",state="down"} 0.0
# HELP neutron_agents Openstack Neutron agent statistic
# TYPE neutron_agents gauge
neutron_agents{host="",region="RegionOne",service="neutron-l3-agent",state="up"} 1.0
# HELP neutron_agents_percent Openstack Neutron agent statistic
# TYPE neutron_agents_percent gauge
neutron_agents_percent{host="",region="RegionOne",service="neutron-dhcp-agent",state="down"} 0.0
# HELP neutron_agents_percent Openstack Neutron agent statistic
# TYPE neutron_agents_percent gauge
neutron_agents_percent{host="",region="RegionOne",service="neutron-metadata-agent",state="down"} 0.0
# HELP neutron_agents Openstack Neutron agent statistic
# TYPE neutron_agents gauge
neutron_agents{host="",region="RegionOne",service="neutron-dhcp-agent",state="disabled"} 0.0
# HELP neutron_agents Openstack Neutron agent statistic
# TYPE neutron_agents gauge
neutron_agents{host="",region="RegionOne",service="neutron-metadata-agent",state="disabled"} 0.0
# HELP neutron_agents Openstack Neutron agent statistic
# TYPE neutron_agents gauge
neutron_agents{host="",region="RegionOne",service="neutron-dhcp-agent",state="up"} 1.0
# HELP neutron_agents Openstack Neutron agent statistic
# TYPE neutron_agents gauge
neutron_agents{host="",region="RegionOne",service="neutron-openvswitch-agent",state="disabled"} 0.0
# HELP neutron_agents_percent Openstack Neutron agent statistic
# TYPE neutron_agents_percent gauge
neutron_agents_percent{host="",region="RegionOne",service="neutron-metadata-agent",state="up"} 100.0
# HELP neutron_agents Openstack Neutron agent statistic
# TYPE neutron_agents gauge
neutron_agents{host="ubuntu-xenial",region="RegionOne",service="neutron-openvswitch-agent",state="up"} 0.0
# HELP neutron_agents Openstack Neutron agent statistic
# TYPE neutron_agents gauge
neutron_agents{host="",region="RegionOne",service="neutron-l3-agent",state="disabled"} 0.0
# HELP neutron_agents_percent Openstack Neutron agent statistic
# TYPE neutron_agents_percent gauge
neutron_agents_percent{host="",region="RegionOne",service="neutron-l3-agent",state="disabled"} 0.0
# HELP neutron_agents Openstack Neutron agent statistic
# TYPE neutron_agents gauge
neutron_agents{host="",region="RegionOne",service="neutron-l3-agent",state="down"} 0.0
# HELP neutron_agents_percent Openstack Neutron agent statistic
# TYPE neutron_agents_percent gauge
neutron_agents_percent{host="",region="RegionOne",service="neutron-openvswitch-agent",state="up"} 100.0
# HELP neutron_agents Openstack Neutron agent statistic
# TYPE neutron_agents gauge
neutron_agents{host="",region="RegionOne",service="neutron-dhcp-agent",state="down"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="nova-compute",state="up"} 1.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="compute",state="up"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="nova-scheduler",state="disabled"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="conductor",state="down"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="nova-consoleauth-68775cf5c-spxsg",region="RegionOne",service="nova-consoleauth",state="up"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="conductor",state="up"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="conductor",state="disabled"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="nova-scheduler-b55bc6487-shlkw",region="RegionOne",service="nova-scheduler",state="up"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="nova-conductor",state="down"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="nova-compute",state="down"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="conductor",state="disabled"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="scheduler",state="up"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="compute",state="down"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="nova-scheduler",state="down"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="nova-consoleauth",state="down"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="consoleauth",state="disabled"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="nova-compute",state="up"} 100.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="nova-compute",state="disabled"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="nova-conductor",state="disabled"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="compute",state="disabled"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="cert",state="disabled"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="compute",state="down"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="nova-scheduler",state="down"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="scheduler",state="disabled"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="nova-consoleauth",state="down"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="cert",state="disabled"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="cert",state="up"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="consoleauth",state="disabled"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="nova-conductor",state="up"} 1.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="scheduler",state="disabled"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="nova-conductor",state="down"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="nova-scheduler",state="disabled"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="scheduler",state="up"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="conductor",state="down"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="nova-consoleauth",state="up"} 100.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="compute",state="disabled"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="consoleauth",state="up"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="nova-conductor",state="disabled"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="consoleauth",state="down"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="cert",state="up"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="ubuntu-xenial",region="RegionOne",service="nova-compute",state="up"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="consoleauth",state="down"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="consoleauth",state="up"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="nova-scheduler",state="up"} 100.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="nova-compute",state="down"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="nova-scheduler",state="up"} 1.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="scheduler",state="down"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="compute",state="up"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="nova-consoleauth",state="disabled"} 0.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="nova-conductor",state="up"} 100.0
# HELP nova_services_percent Openstack Nova Service statistic
# TYPE nova_services_percent gauge
nova_services_percent{host="",region="RegionOne",service="cert",state="down"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="nova-conductor-64f989b787-xpt2h",region="RegionOne",service="nova-conductor",state="up"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="conductor",state="up"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="nova-compute",state="disabled"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="cert",state="down"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="nova-consoleauth",state="disabled"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="scheduler",state="down"} 0.0
# HELP nova_services Openstack Nova Service statistic
# TYPE nova_services gauge
nova_services{host="",region="RegionOne",service="nova-consoleauth",state="up"} 1.0
# HELP total_running_instances Openstack Hypervisor statistic
# TYPE total_running_instances gauge
total_running_instances{aggregate="",aggregate_id="",host="",region="RegionOne"} 0.0
# HELP free_disk_GB Openstack Hypervisor statistic
# TYPE free_disk_GB gauge
free_disk_GB{aggregate="",aggregate_id="",host="ubuntu-xenial",region="RegionOne"} 9.0
# HELP total_used_disk_GB Openstack Hypervisor statistic
# TYPE total_used_disk_GB gauge
total_used_disk_GB{aggregate="",aggregate_id="",host="",region="RegionOne"} 0.0
# HELP total_running_tasks Openstack Hypervisor statistic
# TYPE total_running_tasks gauge
total_running_tasks{aggregate="",aggregate_id="",host="",region="RegionOne"} 0.0
# HELP free_ram_MB Openstack Hypervisor statistic
# TYPE free_ram_MB gauge
free_ram_MB{aggregate="",aggregate_id="",host="ubuntu-xenial",region="RegionOne"} 15535.0
# HELP total_free_vcpus Openstack Hypervisor statistic
# TYPE total_free_vcpus gauge
total_free_vcpus{aggregate="",aggregate_id="",host="",region="RegionOne"} 6.0
# HELP used_ram_MB Openstack Hypervisor statistic
# TYPE used_ram_MB gauge
used_ram_MB{aggregate="",aggregate_id="",host="ubuntu-xenial",region="RegionOne"} 512.0
# HELP total_free_disk_GB Openstack Hypervisor statistic
# TYPE total_free_disk_GB gauge
total_free_disk_GB{aggregate="",aggregate_id="",host="",region="RegionOne"} 9.0
# HELP used_vcpus Openstack Hypervisor statistic
# TYPE used_vcpus gauge
used_vcpus{aggregate="",aggregate_id="",host="ubuntu-xenial",region="RegionOne"} 0.0
# HELP running_tasks Openstack Hypervisor statistic
# TYPE running_tasks gauge
running_tasks{aggregate="",aggregate_id="",host="ubuntu-xenial",region="RegionOne"} 0.0
# HELP used_disk_GB Openstack Hypervisor statistic
# TYPE used_disk_GB gauge
used_disk_GB{aggregate="",aggregate_id="",host="ubuntu-xenial",region="RegionOne"} 0.0
# HELP total_used_vcpus Openstack Hypervisor statistic
# TYPE total_used_vcpus gauge
total_used_vcpus{aggregate="",aggregate_id="",host="",region="RegionOne"} 0.0
# HELP running_instances Openstack Hypervisor statistic
# TYPE running_instances gauge
running_instances{aggregate="",aggregate_id="",host="ubuntu-xenial",region="RegionOne"} 0.0
# HELP free_vcpus Openstack Hypervisor statistic
# TYPE free_vcpus gauge
free_vcpus{aggregate="",aggregate_id="",host="ubuntu-xenial",region="RegionOne"} 6.0
# HELP total_free_ram_MB Openstack Hypervisor statistic
# TYPE total_free_ram_MB gauge
total_free_ram_MB{aggregate="",aggregate_id="",host="",region="RegionOne"} 15535.0
# HELP total_used_ram_MB Openstack Hypervisor statistic
# TYPE total_used_ram_MB gauge
total_used_ram_MB{aggregate="",aggregate_id="",host="",region="RegionOne"} 512.0

```
