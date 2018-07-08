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

from nectarallocationclient.v1 import zones

from nectarallocationclient.tests.unit import utils
from nectarallocationclient.tests.unit.v1 import fakes


class ZonesTest(utils.TestCase):

    def setUp(self):
        super(ZonesTest, self).setUp()
        self.cs = fakes.FakeClient()

    def test_zone_list(self):
        al = self.cs.zones.list()
        self.cs.assert_called('GET', '/zones/')
        for a in al:
            self.assertIsInstance(a, zones.Zone)
        self.assertEqual(2, len(al))

    def test_zone_get(self):
        a = self.cs.zones.get('australia')
        self.cs.assert_called('GET', '/zones/australia/')
        self.assertIsInstance(a, zones.Zone)
        self.assertEqual('australia', a.name)
