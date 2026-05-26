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

from nectarallocationclient.v1 import chiefinvestigators

from nectarallocationclient.tests.unit import utils
from nectarallocationclient.tests.unit.v1 import fakes


class ChiefInvestigatorsTest(utils.TestCase):
    def setUp(self):
        super().setUp()
        self.cs = fakes.FakeClient()

    def test_ci_list(self):
        al = self.cs.chiefinvestigators.list()
        self.cs.assert_called('GET', '/chiefinvestigators/')
        for a in al:
            self.assertIsInstance(a, chiefinvestigators.ChiefInvestigator)
        self.assertEqual(1, len(al))

    def test_ci_get(self):
        a = self.cs.chiefinvestigators.get('1')
        self.cs.assert_called('GET', '/chiefinvestigators/1/')
        self.assertEqual('Smith', a.surname)

    def test_ci_create(self):
        a = self.cs.chiefinvestigators.create(
            allocation=123,
            title='Prof',
            given_name='John',
            surname='Doe',
            email='john@example.org',
            primary_organisation=1,
        )
        self.cs.assert_called('POST', '/chiefinvestigators/')
        self.assertEqual(2, a.id)

    def test_ci_update(self):
        a = self.cs.chiefinvestigators.update('1', title='Prof')
        self.cs.assert_called('PATCH', '/chiefinvestigators/1/')
        self.assertEqual('Prof', a.title)

    def test_ci_delete(self):
        self.cs.chiefinvestigators.delete('1')
        self.cs.assert_called('DELETE', '/chiefinvestigators/1/')
