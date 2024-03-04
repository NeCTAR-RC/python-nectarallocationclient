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

from nectarallocationclient.v1 import bundles

from nectarallocationclient.tests.unit import utils
from nectarallocationclient.tests.unit.v1 import fakes


class BundlesTest(utils.TestCase):

    def setUp(self):
        super(BundlesTest, self).setUp()
        self.cs = fakes.FakeClient()

    def test_bundle_list(self):
        bl = self.cs.bundles.list()
        self.cs.assert_called('GET', '/bundles/')
        for b in bl:
            self.assertIsInstance(b, bundles.Bundle)
        self.assertEqual(2, len(bl))

    def test_bundle_get(self):
        b = self.cs.bundles.get(1)
        self.cs.assert_called('GET', '/bundles/1/')
        self.assertIsInstance(b, bundles.Bundle)
        self.assertEqual('bronze', b.name)
        self.assertEqual(2, len(b.quotas))
        for bq in b.quotas:
            self.assertIsInstance(bq, bundles.BundleQuota)
