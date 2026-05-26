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


class Resource(base.Resource):
    pass


class ResourceManager(base.BasicManager):
    base_url = 'resources'
    resource_class = Resource

    def create(
        self,
        name,
        service_type,
        quota_name,
        unit,
        requestable=True,
        resource_type='integer',
        help_text='',
    ):
        data = {
            'name': name,
            'service_type': base.getid(service_type),
            'quota_name': quota_name,
            'unit': unit,
            'requestable': requestable,
            'resource_type': resource_type,
            'help_text': help_text,
        }
        return self._create(f'/{self.base_url}/', data=data)

    def update(self, resource_id, **kwargs):
        return self._update(f'/{self.base_url}/{resource_id}/', data=kwargs)
