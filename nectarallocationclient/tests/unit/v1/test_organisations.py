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

from nectarallocationclient.v1 import organisations

from nectarallocationclient.tests.unit import utils
from nectarallocationclient.tests.unit.v1 import fakes


class OrganisationsTest(utils.TestCase):
    def setUp(self):
        super().setUp()
        self.cs = fakes.FakeClient()

    def test_organisations_list(self):
        org_list = self.cs.organisations.list()
        self.cs.assert_called('GET', '/organisations/')
        for org in org_list:
            self.assertIsInstance(org, organisations.Organisation)
        self.assertEqual(2, len(org_list))

    def test_organisation_get(self):
        org = self.cs.organisations.get('1')
        self.cs.assert_called('GET', f'/organisations/{org.id}/')
        self.assertIsInstance(org, organisations.Organisation)
        self.assertEqual('KU', org.short_name)
        self.assertEqual('Kanmantoo University', org.full_name)

    def test_organisation_approve(self):
        res = self.cs.organisations.approve('2')
        self.cs.assert_called('POST', '/organisations/2/approve/')
        self.assertIsNone(res)

    def test_organisation_decline(self):
        res = self.cs.organisations.decline('2')
        self.cs.assert_called('POST', '/organisations/2/decline/')
        self.assertIsNone(res)
