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


class Approver(base.Resource):
    pass


class ApproverManager(base.BasicManager):
    base_url = 'approvers'
    resource_class = Approver

    def create(self, username, display_name, sites=None):
        data = {
            'username': username,
            'display_name': display_name,
            'sites': [base.getid(s) for s in sites] if sites else [],
        }
        return self._create(f'/{self.base_url}/', data=data)

    def update(self, resource_id, **kwargs):
        return self._update(f'/{self.base_url}/{resource_id}/', data=kwargs)
