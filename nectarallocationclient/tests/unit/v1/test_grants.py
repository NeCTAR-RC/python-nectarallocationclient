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

from nectarallocationclient.v1 import grants

from nectarallocationclient.tests.unit import utils
from nectarallocationclient.tests.unit.v1 import fakes


class GrantsTest(utils.TestCase):
    def setUp(self):
        super().setUp()
        self.cs = fakes.FakeClient()

    def test_grant_list(self):
        al = self.cs.grants.list()
        self.cs.assert_called('GET', '/grants/')
        for a in al:
            self.assertIsInstance(a, grants.Grant)
        self.assertEqual(1, len(al))

    def test_grant_get(self):
        a = self.cs.grants.get('1')
        self.cs.assert_called('GET', '/grants/1/')
        self.assertEqual('DP123', a.grant_id)

    def test_grant_create(self):
        a = self.cs.grants.create(
            allocation=123,
            grant_type='nhmrc',
            grant_subtype='nhmrc-investigator',
            funding_body_scheme='NHMRC',
            grant_id='GR2',
            first_year_funded=2021,
            last_year_funded=2024,
            total_funding=200000,
        )
        self.cs.assert_called('POST', '/grants/')
        self.assertEqual(2, a.id)

    def test_grant_delete(self):
        self.cs.grants.delete('1')
        self.cs.assert_called('DELETE', '/grants/1/')
