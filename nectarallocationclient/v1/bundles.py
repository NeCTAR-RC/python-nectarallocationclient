#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

from nectarallocationclient import base


class BundleQuota(base.Resource):
    pass


class Bundle(base.Resource):

    def __init__(self, manager, info, loaded=False, resp=None):
        super().__init__(manager, info, loaded, resp)
        raw_quotas = self.quotas
        self.quotas = []
        for quota in raw_quotas:
            self.quotas.append(BundleQuota(manager, quota))


class BundleManager(base.BasicManager):

    base_url = 'bundles'
    resource_class = Bundle
