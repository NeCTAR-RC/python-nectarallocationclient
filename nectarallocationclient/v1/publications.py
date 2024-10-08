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


class Publication(base.Resource):
    pass


class PublicationManager(base.BasicManager):
    base_url = 'publications'
    resource_class = Publication

    def delete(self, resource_id):
        self._delete(f'/{self.base_url}/{resource_id}/')

    def create(self, allocation, publication):
        data = {
            'allocation': base.getid(allocation),
            'publication': publication,
        }
        return self._create(f'/{self.base_url}/', data=data)
