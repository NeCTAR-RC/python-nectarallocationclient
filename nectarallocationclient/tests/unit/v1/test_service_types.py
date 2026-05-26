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

from nectarallocationclient.v1 import service_types

from nectarallocationclient.tests.unit import utils
from nectarallocationclient.tests.unit.v1 import fakes


class ServiceTypesTest(utils.TestCase):
    def setUp(self):
        super().setUp()
        self.cs = fakes.FakeClient()

    def test_service_type_create(self):
        st = self.cs.service_types.create(
            catalog_name='compute', name='Compute'
        )
        self.cs.assert_called('POST', '/service-types/')
        self.assertIsInstance(st, service_types.ServiceType)
        self.assertEqual('compute', st.catalog_name)

    def test_service_type_update(self):
        st = self.cs.service_types.update('compute', name='Compute Updated')
        self.cs.assert_called('PATCH', '/service-types/compute/')
        self.assertEqual('Compute Updated', st.name)
