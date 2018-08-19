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


class ChiefInvestigator(base.Resource):
    pass


class ChiefInvestigatorManager(base.BasicManager):

    base_url = 'chiefinvestigators'
    resource_class = ChiefInvestigator

    def delete(self, resource_id):
        self._delete('/%s/%s/' % (self.base_url, resource_id))

    def create(self, allocation, title, given_name, surname, email,
               institution, additional_researchers=''):
        data = {
            'allocation': base.getid(allocation),
            'title': title,
            'given_name': given_name,
            'surname': surname,
            'email': email,
            'institution': institution,
            'additional_researchers': additional_researchers
        }
        return self._create('/%s/' % self.base_url, data=data)
