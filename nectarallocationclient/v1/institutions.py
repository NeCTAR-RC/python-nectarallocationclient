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


class Institution(base.Resource):
    pass


class InstitutionManager(base.BasicManager):

    base_url = 'institutions'
    resource_class = Institution

    def delete(self, resource_id):
        self._delete('/%s/%s/' % (self.base_url, resource_id))

    def create(self, allocation, name):
        data = {
            'allocation': base.getid(allocation),
            'name': name,
        }
        return self._create('/%s/' % self.base_url, data=data)
