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


class Zone(base.Resource):
    pass


class ZoneManager(base.BasicManager):

    base_url = 'zones'
    resource_class = Zone

    def compute_homes(self):
        return self._get('/%s/compute_homes/' % self.base_url, return_raw=True)
