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


class Organisation(base.Resource):
    pass


class OrganisationManager(base.BasicManager):
    base_url = 'organisations'
    resource_class = Organisation

    def create(self, ror_id='', full_name=None, short_name=None,
               url='', country='AU', proposed_by=None, vetted_by=None,
               parent=None, precedes=None, enabled=True):
        data = {
            'ror_id': ror_id,
            'full_name': full_name,
            'short_name': short_name,
            'url': url,
            'country': country,
            'parent': parent,
            'precedes': precedes,
            'proposed_by': proposed_by,
            'vetted_by': vetted_by,
            'enabled': enabled,
        }
        return self._create("/%s/" % self.base_url, data=data)

    def approve(self, id):
        self._create("/%s/%s/approve/" % (self.base_url, id))

    def decline(self, id):
        self._create("/%s/%s/decline/" % (self.base_url, id))
