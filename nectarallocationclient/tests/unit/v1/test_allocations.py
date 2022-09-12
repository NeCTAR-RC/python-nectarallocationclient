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

from nectarallocationclient import exceptions
from nectarallocationclient.v1 import allocations

from nectarallocationclient.tests.unit import utils
from nectarallocationclient.tests.unit.v1 import fakes


class AllocationsTest(utils.TestCase):

    def setUp(self):
        super(AllocationsTest, self).setUp()
        self.cs = fakes.FakeClient()

    def test_allocation_list(self):
        al = self.cs.allocations.list()
        self.cs.assert_called('GET', '/allocations/')
        for a in al:
            self.assertIsInstance(a, allocations.Allocation)
        self.assertEqual(3, len(al))

    def test_allocation_list_filter(self):
        al = self.cs.allocations.list(project_id='123')
        self.cs.assert_called('GET', '/allocations/',
                              params={'project_id': '123'})
        for a in al:
            self.assertIsInstance(a, allocations.Allocation)
            self.assertEqual('123', a.project_id)
        self.assertEqual(2, len(al))

    def test_allocation_get(self):
        a = self.cs.allocations.get(123)
        self.cs.assert_called('GET', '/allocations/123/')
        self.assertIsInstance(a, allocations.Allocation)
        self.assertEqual(123, a.id)

    def test_allocation_get_current(self):
        a = self.cs.allocations.get_current(project_id='123')
        params = {'project_id': '123',
                  'parent_request__isnull': True}
        self.cs.assert_called('GET', '/allocations/', params=params)
        self.assertIsInstance(a, allocations.Allocation)
        self.assertEqual(587, a.id)

    def test_allocation_get_current_404(self):
        self.assertRaises(exceptions.AllocationDoesNotExist,
                         self.cs.allocations.get_current, project_id='XYZ')
        params = {'project_id': 'XYZ',
                  'parent_request__isnull': True}
        self.cs.assert_called('GET', '/allocations/', params=params)

    def test_get_last_approved(self):
        a = self.cs.allocations.get_last_approved(project_id='123')
        params = {'project_id': '123',
                  'status': 'A'}
        self.cs.assert_called('GET', '/allocations/', params=params)
        self.assertIsInstance(a, allocations.Allocation)
        self.assertEqual('A', a.status)

    def test_update(self):
        a = self.cs.allocations.update(123, notes='test')
        self.cs.assert_called('PATCH', '/allocations/123/', {'notes': 'test'})
        self.assertIsInstance(a, allocations.Allocation)
        self.assertEqual('test', a.notes)

    def test_create(self):
        data = {
            'project_name': 'foo',
            'project_description': 'bar',
            'associated_site': 'qcif',
            'national': True,
            'use_case': 'testing',
            'estimated_number_users': 2,
            'estimated_project_duration': 4,
            'field_of_research_1': 1222,
            'field_of_research_2': 1333,
            'field_of_research_3': 4555,
            'for_percentage_1': 60,
            'for_percentage_2': 30,
            'for_percentage_3': 10,
            'geographic_requirements': 'near the beach',
            'ncris_support': 'some',
            'nectar_support': 'little',
            'usage_patterns': 'sporadic',
            'convert_trial_project': True,
            'notifications': False,
            'managed': False,
        }

        a = self.cs.allocations.create(**data)
        self.cs.assert_called('POST', '/allocations/',
                              data=data)
        self.assertIsInstance(a, allocations.Allocation)

    def test_create_defaults(self):
        data = {
            'project_name': 'foo',
            'project_description': 'bar',
            'use_case': 'testing',
        }
        defaults = {
            'estimated_number_users': 1,
            'estimated_project_duration': 3,
            'field_of_research_1': None,
            'field_of_research_2': None,
            'field_of_research_3': None,
            'for_percentage_1': 0,
            'for_percentage_2': 0,
            'for_percentage_3': 0,
            'geographic_requirements': '',
            'ncris_support': '',
            'nectar_support': '',
            'usage_patterns': '',
            'convert_trial_project': False,
            'notifications': True,
            'associated_site': None,
            'national': False,
            'notifications': True,
            'managed': True,
        }

        a = self.cs.allocations.create(**data)
        data.update(defaults)
        self.cs.assert_called('POST', '/allocations/',
                              data=data)
        self.assertIsInstance(a, allocations.Allocation)

    def test_approve(self):
        a = self.cs.allocations.approve(123)
        self.cs.assert_called('POST', '/allocations/123/approve/')
        self.assertIsInstance(a, allocations.Allocation)

    def test_delete(self):
        a = self.cs.allocations.delete(123)
        self.cs.assert_called('POST', '/allocations/123/delete/')
        self.assertIsInstance(a, allocations.Allocation)

    def test_amend(self):
        a = self.cs.allocations.amend(123)
        self.cs.assert_called('POST', '/allocations/123/amend/')
        self.assertIsInstance(a, allocations.Allocation)

    def test_approver_info(self):
        res = self.cs.allocations.get_approver_info(123)
        self.cs.assert_called('GET', '/allocations/123/approver_info/')
        self.assertEqual(res, {'approval_urgency': 'N/A',
                               'expiry_state': 'None',
                               'concerned_sites': ['ardc']})

    def test_get_allocated_nova_quota(self):
        a = self.cs.allocations.get(123)
        quota = a.get_allocated_nova_quota()
        self.assertEqual({'cores': 4, 'instances': 2, 'ram': 50},
                         quota)

    def test_get_allocated_nova_quota_default_ram(self):
        a = self.cs.allocations.get(124)
        quota = a.get_allocated_nova_quota()
        self.assertEqual({'cores': 4, 'instances': 2, 'ram': 16},
                         quota)

    def test_get_allocated_nova_quota_unlimited_default_ram(self):
        a = self.cs.allocations.get(125)
        quota = a.get_allocated_nova_quota()
        self.assertEqual({'cores': -1, 'instances': 2, 'ram': -1},
                         quota)

    def test_get_allocated_neutron_quota(self):
        a = self.cs.allocations.get(123)
        quota = a.get_allocated_neutron_quota()
        self.assertEqual({'floatingip': 5, 'network': 4, 'router': 3,
                          'subnet': 4},
                         quota)

    def test_get_allocated_octavia_quota(self):
        a = self.cs.allocations.get(123)
        quota = a.get_allocated_octavia_quota()
        self.assertEqual({'load_balancers': 7}, quota)

    def test_get_allocated_magnum_quota(self):
        a = self.cs.allocations.get(123)
        quota = a.get_allocated_magnum_quota()
        self.assertEqual({'clusters': 1}, quota)

    def test_get_allocated_trove_quota(self):
        a = self.cs.allocations.get(123)
        quota = a.get_allocated_trove_quota()
        self.assertEqual({'volumes': 40, 'ram': 8}, quota)

    def test_get_allocated_cloudkitty_quota(self):
        a = self.cs.allocations.get(123)
        quota = a.get_allocated_cloudkitty_quota()
        self.assertEqual({'budget': 56}, quota)

    def test_get_allocated_warre_quota(self):
        a = self.cs.allocations.get(123)
        quota = a.get_allocated_warre_quota()
        self.assertEqual({'days': 2, 'flavor:gpu-v1': True, 'hours': 48,
                          'reservation': 10}, quota)
