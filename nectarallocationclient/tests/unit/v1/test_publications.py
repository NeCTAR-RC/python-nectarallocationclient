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

from nectarallocationclient.v1 import publications

from nectarallocationclient.tests.unit import utils
from nectarallocationclient.tests.unit.v1 import fakes


class PublicationsTest(utils.TestCase):
    def setUp(self):
        super().setUp()
        self.cs = fakes.FakeClient()

    def test_publication_list(self):
        al = self.cs.publications.list()
        self.cs.assert_called('GET', '/publications/')
        for a in al:
            self.assertIsInstance(a, publications.Publication)
        self.assertEqual(1, len(al))

    def test_publication_get(self):
        a = self.cs.publications.get('1')
        self.cs.assert_called('GET', '/publications/1/')
        self.assertEqual('A great paper', a.publication)

    def test_publication_create(self):
        a = self.cs.publications.create(
            allocation=123,
            output_type='AJ',
            publication='Another paper',
            doi='10.1234/abc',
        )
        self.cs.assert_called('POST', '/publications/')
        self.assertEqual(2, a.id)

    def test_publication_delete(self):
        self.cs.publications.delete('1')
        self.cs.assert_called('DELETE', '/publications/1/')
