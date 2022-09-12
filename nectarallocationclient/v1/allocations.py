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

import logging

from nectarallocationclient import base
from nectarallocationclient import exceptions
from nectarallocationclient import states
from nectarallocationclient.v1 import quotas


LOG = logging.getLogger(__name__)


class Allocation(base.Resource):

    def __init__(self, manager, info, loaded=False, resp=None):
        super(Allocation, self).__init__(manager, info, loaded, resp)
        raw_quotas = self.quotas
        self.quotas = []
        self._quota_cache = None
        for quota in raw_quotas:
            self.quotas.append(quotas.Quota(manager, quota))

    def __repr__(self):
        return "<Allocation %s (%s)>" % (self.id, self.project_name)

    def approve(self):
        return self.manager.approve(self.id)

    def amend(self):
        return self.manager.amend(self.id)

    def update(self, **kwargs):
        LOG.debug("%s: Updating allocation %s", self.id, kwargs)
        return self.manager.update(self.id, **kwargs)

    def delete(self):
        LOG.debug("%s: Deleting allocation", self.id)
        return self.manager.delete(self.id)

    def get_approver_info(self):
        return self.manager.get_approver_info(self.id)

    def get_quota(self, service_type):
        if self._quota_cache is None:
            service_types = {}
            for quota in self.quotas:
                st, resource = quota.resource.split('.')
                if st in service_types:
                    service_types[st].append(quota)
                else:
                    service_types[st] = [quota]
            self._quota_cache = service_types

        try:
            return self._quota_cache[service_type]
        except KeyError:
            return []

    def get_allocated_cloudkitty_quota(self):
        quotas = self.get_quota('rating')
        if not quotas:
            return {}
        kwargs = {}
        for quota in quotas:
            quota_resource = quota.resource.split('.')[1]
            kwargs[quota_resource] = quota.quota

        return kwargs

    def get_allocated_nova_quota(self):
        quotas = self.get_quota('compute')
        if not quotas:
            return {}
        kwargs = {}
        for quota in quotas:
            quota_resource = quota.resource.split('.')[1]
            kwargs[quota_resource] = quota.quota
        if not kwargs.get('cores') or not kwargs.get('instances'):
            return {}
        if 'ram' not in kwargs or int(kwargs['ram']) == 0:
            if kwargs['cores'] == -1:
                kwargs['ram'] = -1
            else:
                kwargs['ram'] = kwargs['cores'] * 4
        return kwargs

    def get_allocated_cinder_quota(self):
        kwargs = {}
        total = 0

        quotas = self.get_quota('volume')
        if not quotas:
            return {}
        for quota in quotas:
            kwargs["volumes_%s" % (quota.zone)] = quota.quota
            kwargs["gigabytes_%s" % (quota.zone)] = quota.quota
            kwargs["snapshots_%s" % (quota.zone)] = quota.quota
            total += quota.quota
        kwargs['volumes'] = total
        kwargs['gigabytes'] = total
        kwargs['snapshots'] = total
        return kwargs

    def get_allocated_swift_quota(self):
        quotas = self.get_quota('object')
        if len(quotas) > 1:
            raise
        if quotas:
            gigabytes = int(quotas[0].quota)
        else:
            gigabytes = 0
        return {'object': gigabytes}

    def get_allocated_trove_quota(self):
        quotas = self.get_quota('database')
        if not quotas:
            return {}
        kwargs = {}
        for quota in quotas:
            quota_resource = quota.resource.split('.')[1]
            kwargs[quota_resource] = quota.quota

        if 'ram' not in kwargs or int(kwargs['ram']) == 0:
            kwargs['ram'] = 8
        if 'volumes' not in kwargs:
            kwargs['volumes'] = int(kwargs['ram']) * 5
        return kwargs

    def get_allocated_manila_quota(self):
        kwargs = {}
        kwargs = {'shares': 0, 'gigabytes': 0,
                  'snapshots': 0, 'snapshot_gigabytes': 0}

        quotas = self.get_quota('share')
        for quota in quotas:
            quota_resource = quota.resource.split('.')[1]
            kwargs["%s_%s" % (quota_resource, quota.zone)] = quota.quota
            kwargs[quota_resource] += quota.quota
        return kwargs

    def get_allocated_neutron_quota(self):
        quotas = self.get_quota('network')
        if not quotas:
            return {}
        kwargs = {}
        for quota in quotas:
            quota_resource = quota.resource.split('.')[1]
            kwargs[quota_resource] = quota.quota
        if 'network' in kwargs:
            kwargs['subnet'] = kwargs['network']
        kwargs.pop('loadbalancer', None)
        return kwargs

    def get_allocated_octavia_quota(self):
        # Get LB quota from network group for now
        quotas = self.get_quota('network')
        if not quotas:
            return {}
        kwargs = {}
        for quota in quotas:
            quota_resource = quota.resource.split('.')[1]
            if quota_resource == 'loadbalancer':
                kwargs['load_balancers'] = quota.quota
        return kwargs

    def get_allocated_magnum_quota(self):
        quotas = self.get_quota('container-infra')
        if not quotas:
            return {}
        kwargs = {}
        for quota in quotas:
            quota_resource = quota.resource.split('.')[1]
            kwargs[quota_resource] = quota.quota
        return kwargs

    def get_allocated_warre_quota(self):
        quotas = self.get_quota('nectar-reservation')
        if not quotas:
            return {}
        kwargs = {}
        for quota in quotas:
            quota_resource = quota.resource.split('.')[1]
            if quota_resource == 'days':
                kwargs['hours'] = quota.quota * 24
            kwargs[quota_resource] = quota.quota
        return kwargs


class AllocationManager(base.Manager):

    resource_class = Allocation

    def list(self, **kwargs):
        return self._list('/allocations/', params=kwargs)

    def get(self, allocation_id):
        return self._get('/allocations/%s/' % allocation_id)

    def get_current(self, **kwargs):
        kwargs['parent_request__isnull'] = True
        allocations = self.list(**kwargs)

        if len(allocations) == 1:
            return allocations[0]
        elif len(allocations) == 0:
            raise exceptions.AllocationDoesNotExist()
        else:
            ids = [x.id for x in allocations]
            raise ValueError("More than one allocation returned: %s" % ids)

    def get_last_approved(self, **kwargs):
        allocations = self.list(status=states.APPROVED, **kwargs)
        if allocations:
            return allocations[0]
        raise exceptions.AllocationDoesNotExist()

    def update(self, allocation_id, **kwargs):
        return self._update('/allocations/%s/' % allocation_id, data=kwargs)

    def create(self, project_name, project_description,
               allocation_home=None, use_case=None,
               estimated_number_users=1, estimated_project_duration=3,
               field_of_research_1=None, field_of_research_2=None,
               field_of_research_3=None,
               for_percentage_1=0, for_percentage_2=0, for_percentage_3=0,
               geographic_requirements='', ncris_support='', nectar_support='',
               usage_patterns='', convert_trial_project=False,
               associated_site=None, national=False, notifications=True,
               managed=True):
        # Backwards compatibility logic for 'allocation_home' is handled
        # server-side. Maybe we should warn the app that they are
        # using a deprecated feature
        if not use_case:
            # Unfortunately, we had to turn 'use_case' into a keyword
            # argument for compatibility reasons.  But we don't want
            # empty values.
            raise ValueError("A non-empty 'use_case' is mandatory")
        data = {
            'project_name': project_name,
            'project_description': project_description,
            'convert_trial_project': convert_trial_project,
            'associated_site': associated_site,
            'national': national,
            'use_case': use_case,
            'estimated_number_users': estimated_number_users,
            'estimated_project_duration': estimated_project_duration,
            'field_of_research_1': field_of_research_1,
            'field_of_research_2': field_of_research_2,
            'field_of_research_3': field_of_research_3,
            'for_percentage_1': for_percentage_1,
            'for_percentage_2': for_percentage_2,
            'for_percentage_3': for_percentage_3,
            'geographic_requirements': geographic_requirements,
            'ncris_support': ncris_support,
            'nectar_support': nectar_support,
            'usage_patterns': usage_patterns,
            'notifications': notifications,
            'managed': managed,
        }
        return self._create('/allocations/', data=data)

    def approve(self, allocation_id):
        return self._create('/allocations/%s/approve/' % allocation_id)

    def delete(self, allocation_id):
        return self._create('/allocations/%s/delete/' % allocation_id)

    def amend(self, allocation_id):
        return self._create('/allocations/%s/amend/' % allocation_id)

    def get_approver_info(self, allocation_id):
        return self._get('/allocations/%s/approver_info/' % allocation_id,
                         return_raw=True)
