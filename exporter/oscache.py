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

from threading import Thread
from threading import Lock
import pickle
from prometheus_client import CollectorRegistry, generate_latest, Gauge, CONTENT_TYPE_LATEST
from os import environ as env
from os import rename, path
from time import sleep, time
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)

class ThreadSafeDict(dict) :
    def __init__(self, * p_arg, ** n_arg) :
        dict.__init__(self, * p_arg, ** n_arg)
        self._lock = Lock()

    def __enter__(self) :
        self._lock.acquire()
        return self

    def __exit__(self, type, value, traceback) :
        self._lock.release()

class OSCache(Thread):

    def __init__(self, refresh_interval, region):
        Thread.__init__(self)
        self.daemon = True
        self.duration = 0
        self.refresh_interval = refresh_interval
        self.cache = ThreadSafeDict()
        self.region = region
        self.osclients = []

    def cache_me(self, osclient):
        self.osclients.append(osclient)
        logger.debug("new osclient added to cache")

    def run(self):
        while True:
            start_time = time()
            for osclient in self.osclients:
                try:
                    self.cache[osclient.get_cache_key()] = osclient.build_cache_data()
                except Exception as e:
                    logger.error(str(e))
                    logger.error("failed to get data for cache key {}".format(osclient.get_cache_key()))
            self.duration = time() - start_time
            sleep(self.refresh_interval)

    def get_cache_data(self, key):
        if key in self.cache:
            return self.cache[key]
        else:
            return []

    def get_stats(self):
        registry = CollectorRegistry()
        labels = ['region']
        label_values = [self.region]
        duration = Gauge('openstack_exporter_cache_refresh_duration_seconds',
                         'Cache refresh duration in seconds.',
                         labels, registry=registry)
        duration.labels(*label_values).set(self.duration)
        return generate_latest(registry)
