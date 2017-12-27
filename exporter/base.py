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

import re

class OSBase(object):
    FAIL = 0
    OK = 1
    UNKNOWN = 2

    def __init__(self, oscache, osclient):
        self.oscache = oscache
        self.osclient = osclient
        self.oscache.cache_me(self)

    def get_cache_data(self):
        return self.oscache.get_cache_data(self.get_cache_key())

    def build_cache_data(self):
        """ build a hash to store in cache """
        raise NotImplemented("Must be implemented by the subclass!")

    def get_cache_key(self):
        """ cache key """
        raise NotImplemented("Must be implemented by the subclass!")

    def get_stats(self):
        """ build stats for prometheus exporter """
        raise NotImplemented("Must be implemented by the subclass!")

    def gauge_name_sanitize(self, input):
        return re.sub(r'[^a-zA-Z0-9:_]', '_', input)
