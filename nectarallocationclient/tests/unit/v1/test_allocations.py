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
            'start_date': '2018-03-03',
            'allocation_home': 'somewhere',
            'use_case': 'testing',
        }

        a = self.cs.allocations.create(**data)
        data['convert_trial_project'] = False
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
