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

from nectarallocationclient.v1 import quotas

from nectarallocationclient.tests.unit import utils
from nectarallocationclient.tests.unit.v1 import fakes


class QuotasTest(utils.TestCase):

    def setUp(self):
        super(QuotasTest, self).setUp()
        self.cs = fakes.FakeClient()

    def test_quota_list(self):
        ql = self.cs.quotas.list()
        self.cs.assert_called('GET', '/quotas/')
        for q in ql:
            self.assertIsInstance(q, quotas.Quota)
        self.assertEqual(2, len(ql))

    def test_quota_get(self):
        q = self.cs.quotas.get(1)
        self.cs.assert_called('GET', '/quotas/1/')
        self.assertIsInstance(q, quotas.Quota)
        self.assertEqual(1, q.id)

    def test_quota_delete(self):
        self.cs.quotas.delete(1)
        self.cs.assert_called('DELETE', '/quotas/1/')

    def test_quota_create(self):
        q = self.cs.quotas.create(allocation=2, resource=4, quota=3,
                                  zone='foo')
        self.cs.assert_called('POST', '/quotas/',
                              data={'allocation': 2, 'resource': 4,
                                    'zone': 'foo', 'quota': 3,
                                    'requested_quota': 3})
        self.assertIsInstance(q, quotas.Quota)
