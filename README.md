Prometheus Openstack Exporter
============

Image for a prometheus exporter for openstack API derived metrics.

## Environment

check sample env file provided in the source.

* OS USERNAME
  - username associated with the monitoring tenant/project in openstack, used for polling openstack API, **required**

* OS PASSWORD
  - password for the username associated with the monitoring tenant/project in openstack, used for polling openstack API, **required**

* OS PROJECT NAME
  - monitoring tenant/project in openstack, used for polling openstack API, **required**

* OS AUTH URL
  - openstack keystone API endpoint, **required**

* LISTEN PORT
  - port to bind for prometheus scrape target

* OS REGION NAME
  - openstack region to use keystone service catalog against

* TIMEOUT SECONDS
  - number of seconds before API calls should timeout

* OS POLLING INTERVAL
  - interval in seconds between API polls

* OS RETRIES
  - number of retries on API calls before failing

* OS CPU OC RATIO
  - CPU overcommit ratio for the hypervisor

* OS RAM OC RATIO=1
  - RAM overcommit ratio for the hypervisor

## Docker Usage

docker run --env-file sample env file -it rakeshpatnaik/prometheus-openstack-exporter:v0.2

## sample test
docker exec \<instance-id\> curl http://localhost:19103/metrics
```
-------Sample truncated Output----
# HELP openstack_total_used_ram_MB Openstack Hypervisor statistic
# TYPE openstack_total_used_ram_MB gauge
openstack_total_used_ram_MB{aggregate="",aggregate_id="",host="",region="RegionOne"} 6897.0
# HELP openstack_total_used_vcpus Openstack Hypervisor statistic
# TYPE openstack_total_used_vcpus gauge
openstack_total_used_vcpus{aggregate="",aggregate_id="",host="",region="RegionOne"} 0.0
# HELP openstack_used_ram_MB Openstack Hypervisor statistic
# TYPE openstack_used_ram_MB gauge
openstack_used_ram_MB{aggregate="",aggregate_id="",host="ubuntu-xenial",region="RegionOne"} 6897.0
```

## Metrics
Name     | Sample Labels | Sample Value | Description
---------|---------------|--------------|------------
openstack_exporter_cache_refresh_duration_seconds|region="RegionOne"| 0.3854649066925049
openstack_check_neutron_api|region="RegionOne",service="neutron",url="http://neutron-server.openstack.svc.cluster.local:9696"| 1.0
openstack_check_glance_api|region="RegionOne",service="glance",url="http://glance-api.openstack.svc.cluster.local:9292"| 1.0
openstack_check_keystone_api|region="RegionOne",service="keystone",url="http://keystone-api.openstack.svc.cluster.local:80"| 1.0
openstack_check_placement_api|region="RegionOne",service="placement",url="http://placement-api.openstack.svc.cluster.local:8778"| 1.0
openstack_check_swift_api|region="RegionOne",service="swift",url="http://ceph-rgw.ceph.svc.cluster.local:8088"| 1.0
openstack_check_nova_api|region="RegionOne",service="nova",url="http://nova-api.openstack.svc.cluster.local:8774"| 1.0
openstack_services_neutron_neutron_metadata_agent|host="ubuntu-xenial",region="RegionOne",service="neutron-metadata-agent",state="up"| 1.0
openstack_services_neutron_metadata_agent_down_percent|host="",region="RegionOne",service="neutron-metadata-agent",state="down"| 0.0
openstack_services_neutron_openvswitch_agent_up_percent|host="",region="RegionOne",service="neutron-openvswitch-agent",state="up"| 100.0
openstack_services_neutron_l3_agent_disabled_total|host="",region="RegionOne",service="neutron-l3-agent",state="disabled"| 0.0
openstack_services_neutron_dhcp_agent_up_total|host="",region="RegionOne",service="neutron-dhcp-agent",state="up"| 1.0
openstack_services_neutron_dhcp_agent_down_percent|host="",region="RegionOne",service="neutron-dhcp-agent",state="down"| 0.0
openstack_services_neutron_l3_agent_up_percent|host="",region="RegionOne",service="neutron-l3-agent",state="up"| 100.0
openstack_services_neutron_openvswitch_agent_up_total|host="",region="RegionOne",service="neutron-openvswitch-agent",state="up"| 1.0
openstack_services_neutron_neutron_dhcp_agent|host="ubuntu-xenial",region="RegionOne",service="neutron-dhcp-agent",state="up"| 1.0
openstack_services_neutron_openvswitch_agent_down_percent|host="",region="RegionOne",service="neutron-openvswitch-agent",state="down"| 0.0
openstack_services_neutron_dhcp_agent_down_total|host="",region="RegionOne",service="neutron-dhcp-agent",state="down"| 0.0
openstack_services_neutron_metadata_agent_up_percent|host="",region="RegionOne",service="neutron-metadata-agent",state="up"| 100.0
openstack_services_neutron_l3_agent_up_total|host="",region="RegionOne",service="neutron-l3-agent",state="up"| 1.0
openstack_services_neutron_neutron_openvswitch_agent|host="ubuntu-xenial",region="RegionOne",service="neutron-openvswitch-agent",state="up"| 1.0
openstack_services_neutron_metadata_agent_disabled_total|host="",region="RegionOne",service="neutron-metadata-agent",state="disabled"| 0.0
openstack_services_neutron_l3_agent_down_percent|host="",region="RegionOne",service="neutron-l3-agent",state="down"| 0.0
openstack_services_neutron_metadata_agent_up_total|host="",region="RegionOne",service="neutron-metadata-agent",state="up"| 1.0
openstack_services_neutron_openvswitch_agent_down_total|host="",region="RegionOne",service="neutron-openvswitch-agent",state="down"| 0.0
openstack_services_neutron_dhcp_agent_disabled_percent|host="",region="RegionOne",service="neutron-dhcp-agent",state="disabled"| 0.0
openstack_services_neutron_dhcp_agent_disabled_total|host="",region="RegionOne",service="neutron-dhcp-agent",state="disabled"| 0.0
openstack_services_neutron_l3_agent_down_total|host="",region="RegionOne",service="neutron-l3-agent",state="down"| 0.0
openstack_services_neutron_openvswitch_agent_disabled_percent|host="",region="RegionOne",service="neutron-openvswitch-agent",state="disabled"| 0.0
openstack_services_neutron_metadata_agent_disabled_percent|host="",region="RegionOne",service="neutron-metadata-agent",state="disabled"| 0.0
openstack_services_neutron_metadata_agent_down_total|host="",region="RegionOne",service="neutron-metadata-agent",state="down"| 0.0
openstack_services_neutron_l3_agent_disabled_percent|host="",region="RegionOne",service="neutron-l3-agent",state="disabled"| 0.0
openstack_services_neutron_openvswitch_agent_disabled_total|host="",region="RegionOne",service="neutron-openvswitch-agent",state="disabled"| 0.0
openstack_services_neutron_neutron_l3_agent|host="ubuntu-xenial",region="RegionOne",service="neutron-l3-agent",state="up"| 1.0
openstack_services_neutron_dhcp_agent_up_percent|host="",region="RegionOne",service="neutron-dhcp-agent",state="up"| 100.0
openstack_services_nova_conductor_down_total|host="",region="RegionOne",service="nova-conductor",state="down"| 0.0
openstack_services_nova_consoleauth_disabled_percent|host="",region="RegionOne",service="nova-consoleauth",state="disabled"| 0.0
openstack_services_nova_scheduler_down_total|host="",region="RegionOne",service="nova-scheduler",state="down"| 0.0
openstack_services_nova_conductor_disabled_total|host="",region="RegionOne",service="nova-conductor",state="disabled"| 0.0
openstack_services_nova_conductor_down_percent|host="",region="RegionOne",service="nova-conductor",state="down"| 0.0
openstack_services_nova_conductor_disabled_percent|host="",region="RegionOne",service="nova-conductor",state="disabled"| 0.0
openstack_services_nova_nova_conductor|host="nova-conductor-d557644d8-5rh8z",region="RegionOne",service="nova-conductor",state="up"| 1.0
openstack_services_nova_compute_disabled_total|host="",region="RegionOne",service="nova-compute",state="disabled"| 0.0
openstack_services_nova_nova_compute|host="ubuntu-xenial",region="RegionOne",service="nova-compute",state="down"| 0.0
openstack_services_nova_scheduler_disabled_percent|host="",region="RegionOne",service="nova-scheduler",state="disabled"| 0.0
openstack_services_nova_conductor_up_percent|host="",region="RegionOne",service="nova-conductor",state="up"| 100.0
openstack_services_nova_scheduler_up_percent|host="",region="RegionOne",service="nova-scheduler",state="up"| 100.0
openstack_services_nova_consoleauth_up_percent|host="",region="RegionOne",service="nova-consoleauth",state="up"| 100.0
openstack_services_nova_compute_up_percent|host="",region="RegionOne",service="nova-compute",state="up"| 0.0
openstack_services_nova_conductor_up_total|host="",region="RegionOne",service="nova-conductor",state="up"| 1.0
openstack_services_nova_consoleauth_up_total|host="",region="RegionOne",service="nova-consoleauth",state="up"| 1.0
openstack_services_nova_scheduler_disabled_total|host="",region="RegionOne",service="nova-scheduler",state="disabled"| 0.0
openstack_services_nova_consoleauth_disabled_total|host="",region="RegionOne",service="nova-consoleauth",state="disabled"| 0.0
openstack_services_nova_compute_up_total|host="",region="RegionOne",service="nova-compute",state="up"| 0.0
openstack_services_nova_consoleauth_down_percent|host="",region="RegionOne",service="nova-consoleauth",state="down"| 0.0
openstack_services_nova_compute_disabled_percent|host="",region="RegionOne",service="nova-compute",state="disabled"| 0.0
openstack_services_nova_scheduler_up_total|host="",region="RegionOne",service="nova-scheduler",state="up"| 1.0
openstack_services_nova_scheduler_down_percent|host="",region="RegionOne",service="nova-scheduler",state="down"| 0.0
openstack_services_nova_nova_scheduler|host="nova-scheduler-7cbb4b94d8-n88gh",region="RegionOne",service="nova-scheduler",state="up"| 1.0
openstack_services_nova_compute_down_total|host="",region="RegionOne",service="nova-compute",state="down"| 1.0
openstack_services_nova_compute_down_percent|host="",region="RegionOne",service="nova-compute",state="down"| 100.0
openstack_services_nova_nova_consoleauth|host="nova-consoleauth-759864bc4-4tgmm",region="RegionOne",service="nova-consoleauth",state="up"| 1.0
openstack_services_nova_consoleauth_down_total|host="",region="RegionOne",service="nova-consoleauth",state="down"| 0.0
openstack_total_running_instances|aggregate="",aggregate_id="",host="",region="RegionOne"| 0.0
openstack_used_disk_GB|aggregate="",aggregate_id="",host="ubuntu-xenial",region="RegionOne"| 9.0
openstack_free_disk_GB|aggregate="",aggregate_id="",host="ubuntu-xenial",region="RegionOne"| 19.0
openstack_total_running_tasks|aggregate="",aggregate_id="",host="",region="RegionOne"| 0.0
openstack_total_free_ram_MB|aggregate="",aggregate_id="",host="",region="RegionOne"| 15535.0
openstack_running_tasks|aggregate="",aggregate_id="",host="ubuntu-xenial",region="RegionOne"| 0.0
openstack_total_used_disk_GB|aggregate="",aggregate_id="",host="",region="RegionOne"| 9.0
openstack_total_free_vcpus|aggregate="",aggregate_id="",host="",region="RegionOne"| 4.0
openstack_free_vcpus|aggregate="",aggregate_id="",host="ubuntu-xenial",region="RegionOne"| 4.0
openstack_running_instances|aggregate="",aggregate_id="",host="ubuntu-xenial",region="RegionOne"| 0.0
openstack_free_ram_MB|aggregate="",aggregate_id="",host="ubuntu-xenial",region="RegionOne"| 15535.0
openstack_total_free_disk_GB|aggregate="",aggregate_id="",host="",region="RegionOne"| 19.0
openstack_used_vcpus|aggregate="",aggregate_id="",host="ubuntu-xenial",region="RegionOne"| 0.0
openstack_total_used_ram_MB|aggregate="",aggregate_id="",host="",region="RegionOne"| 6897.0
openstack_total_used_vcpus|aggregate="",aggregate_id="",host="",region="RegionOne"| 0.0
openstack_used_ram_MB|aggregate="",aggregate_id="",host="ubuntu-xenial",region="RegionOne"| 6897.0
openstack_check_cinder_api|region="RegionOne",service="cinder",url="http://cinder-api.openstack.svc.cluster.local:8776"| 1.0
openstack_check_cinder_api|region="RegionOne",service="cinder",url="http://cinder-api.openstack.svc.cluster.local:8776"| 1.0
openstack_check_cinder_api|region="RegionOne",service="cinder",url="http://cinder-api.openstack.svc.cluster.local:8776"| 1.0
openstack_services_cinder_scheduler_up_percent|host="",region="RegionOne",service="cinder-scheduler",state="up"| 100.0
openstack_services_cinder_volume_down_total|host="",region="RegionOne",service="cinder-volume",state="down"| 0.0
openstack_services_cinder_volume_up_percent|host="",region="RegionOne",service="cinder-volume",state="up"| 100.0
openstack_services_cinder_scheduler_disabled_total|host="",region="RegionOne",service="cinder-scheduler",state="disabled"| 0.0
openstack_services_cinder_volume_disabled_total|host="",region="RegionOne",service="cinder-volume",state="disabled"| 0.0
openstack_services_cinder_volume_disabled_percent|host="",region="RegionOne",service="cinder-volume",state="disabled"| 0.0
openstack_services_cinder_backup_down_percent|host="",region="RegionOne",service="cinder-backup",state="down"| 0.0
openstack_services_cinder_cinder_scheduler|host="cinder-volume-worker",region="RegionOne",service="cinder-scheduler",state="up"| 1.0
openstack_services_cinder_scheduler_disabled_percent|host="",region="RegionOne",service="cinder-scheduler",state="disabled"| 0.0
openstack_services_cinder_backup_disabled_total|host="",region="RegionOne",service="cinder-backup",state="disabled"| 0.0
openstack_services_cinder_cinder_backup|host="cinder-volume-worker",region="RegionOne",service="cinder-backup",state="up"| 1.0
openstack_services_cinder_scheduler_down_total|host="",region="RegionOne",service="cinder-scheduler",state="down"| 0.0
openstack_services_cinder_backup_down_total|host="",region="RegionOne",service="cinder-backup",state="down"| 0.0
openstack_services_cinder_cinder_volume|host="cinder-volume-worker@rbd1",region="RegionOne",service="cinder-volume",state="up"| 1.0
openstack_services_cinder_backup_up_total|host="",region="RegionOne",service="cinder-backup",state="up"| 1.0
openstack_services_cinder_scheduler_down_percent|host="",region="RegionOne",service="cinder-scheduler",state="down"| 0.0
openstack_services_cinder_volume_up_total|host="",region="RegionOne",service="cinder-volume",state="up"| 1.0
openstack_services_cinder_backup_up_percent|host="",region="RegionOne",service="cinder-backup",state="up"| 100.0
openstack_services_cinder_volume_down_percent|host="",region="RegionOne",service="cinder-volume",state="down"| 0.0
openstack_services_cinder_backup_disabled_percent|host="",region="RegionOne",service="cinder-backup",state="disabled"| 0.0
openstack_services_cinder_scheduler_up_total|host="",region="RegionOne",service="cinder-scheduler",state="up"| 1.0
