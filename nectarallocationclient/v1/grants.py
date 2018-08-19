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


class Grant(base.Resource):
    pass


class GrantManager(base.BasicManager):

    base_url = 'grants'
    resource_class = Grant

    def delete(self, resource_id):
        self._delete('/%s/%s/' % (self.base_url, resource_id))

    def create(self, allocation, grant_type, funding_body_scheme, grant_id,
               first_year_funded, last_year_funded, total_funding):
        data = {
            'allocation': base.getid(allocation),
            'grant_type': grant_type,
            'funding_body_scheme': funding_body_scheme,
            'grant_id': grant_id,
            'first_year_funded': first_year_funded,
            'last_year_funded': last_year_funded,
            'total_funding': total_funding
        }
        return self._create('/%s/' % self.base_url, data=data)
