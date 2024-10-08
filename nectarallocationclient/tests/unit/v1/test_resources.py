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

from nectarallocationclient.v1 import resources

from nectarallocationclient.tests.unit import utils
from nectarallocationclient.tests.unit.v1 import fakes


class ResourcesTest(utils.TestCase):
    def setUp(self):
        super().setUp()
        self.cs = fakes.FakeClient()

    def test_resource_list(self):
        al = self.cs.resources.list()
        self.cs.assert_called('GET', '/resources/')
        for a in al:
            self.assertIsInstance(a, resources.Resource)
        self.assertEqual(3, len(al))

    def test_resource_get(self):
        a = self.cs.resources.get(1)
        self.cs.assert_called('GET', '/resources/1/')
        self.assertIsInstance(a, resources.Resource)
        self.assertEqual(1, a.id)
