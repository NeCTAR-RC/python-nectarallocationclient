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
from nectarallocationclient.v1 import zones


class Quota(base.Resource):
    pass


class QuotaManager(base.Manager):

    base_url = 'quotas'
    resource_class = Quota

    def list(self, **kwargs):
        allocation = kwargs.pop('allocation', None)
        if allocation:
            kwargs['group__allocation'] = base.getid(allocation)
        zone = kwargs.pop('zone', None)
        if zone:
            kwargs['group__zone'] = zone
        service_type = kwargs.pop('service_type', None)
        if service_type:
            kwargs['group__service_type'] = service_type

        return self._list('/%s/' % self.base_url, params=kwargs)

    def get(self, quota_id):
        return self._get('/%s/%s/' % (self.base_url, quota_id))

    def delete(self, quota_id):
        self._delete('/%s/%s/' % (self.base_url, quota_id))

    def create(self, allocation, resource, zone, quota, requested_quota=None):
        if type(zone) == zones.Zone:
            zone = zone.name
        data = {
            'allocation': base.getid(allocation),
            'resource': base.getid(resource),
            'zone': zone,
            'quota': quota,
            'requested_quota': requested_quota or quota,
        }
        return self._create('/%s/' % self.base_url, data=data)
