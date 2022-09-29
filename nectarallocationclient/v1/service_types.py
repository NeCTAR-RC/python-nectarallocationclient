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
from nectarallocationclient.v1 import resources


class ServiceType(base.Resource):

    def __init__(self, manager, info, loaded=False, resp=None):
        super(ServiceType, self).__init__(manager, info, loaded, resp)
        self.resources = []
        for resource in self.resource_set:
            self.resources.append(resources.Resource(manager, resource))
        del self.resource_set

    def __repr__(self):
        return "<ServiceType %s>" % (self.catalog_name)


class ServiceTypeManager(base.BasicManager):

    base_url = 'service-types'
    resource_class = ServiceType
