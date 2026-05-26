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

from nectarallocationclient.v1 import approvers

from nectarallocationclient.tests.unit import utils
from nectarallocationclient.tests.unit.v1 import fakes


class ApproversTest(utils.TestCase):
    def setUp(self):
        super().setUp()
        self.cs = fakes.FakeClient()

    def test_approver_list(self):
        al = self.cs.approvers.list()
        self.cs.assert_called('GET', '/approvers/')
        for a in al:
            self.assertIsInstance(a, approvers.Approver)
        self.assertEqual(2, len(al))

    def test_approver_get(self):
        a = self.cs.approvers.get('1')
        self.cs.assert_called('GET', '/approvers/1/')
        self.assertIsInstance(a, approvers.Approver)
        self.assertEqual('approver1@example.org', a.username)

    def test_approver_create(self):
        a = self.cs.approvers.create(
            username='approver3@example.org',
            display_name='Approver Three',
        )
        self.cs.assert_called('POST', '/approvers/')
        self.assertIsInstance(a, approvers.Approver)
        self.assertEqual(3, a.id)

    def test_approver_update(self):
        a = self.cs.approvers.update('1', display_name='Renamed Approver')
        self.cs.assert_called('PATCH', '/approvers/1/')
        self.assertEqual('Renamed Approver', a.display_name)
