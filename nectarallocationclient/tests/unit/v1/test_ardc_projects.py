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

from nectarallocationclient.v1 import ardc_projects

from nectarallocationclient.tests.unit import utils
from nectarallocationclient.tests.unit.v1 import fakes


class ARDCProjectsTest(utils.TestCase):
    def setUp(self):
        super().setUp()
        self.cs = fakes.FakeClient()

    def test_ardc_project_list(self):
        al = self.cs.ardc_projects.list()
        self.cs.assert_called('GET', '/ardc-projects/')
        for a in al:
            self.assertIsInstance(a, ardc_projects.ARDCProject)
        self.assertEqual(2, len(al))

    def test_ardc_project_get(self):
        a = self.cs.ardc_projects.get('1')
        self.cs.assert_called('GET', '/ardc-projects/1/')
        self.assertIsInstance(a, ardc_projects.ARDCProject)
        self.assertEqual('BioCommons', a.short_name)

    def test_ardc_project_create(self):
        a = self.cs.ardc_projects.create(
            name='New Project', short_name='NP', project_id='AP3'
        )
        self.cs.assert_called('POST', '/ardc-projects/')
        self.assertIsInstance(a, ardc_projects.ARDCProject)
        self.assertEqual(3, a.id)

    def test_ardc_project_update(self):
        a = self.cs.ardc_projects.update('1', enabled=False)
        self.cs.assert_called('PATCH', '/ardc-projects/1/')
        self.assertFalse(a.enabled)
