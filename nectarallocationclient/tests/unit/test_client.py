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

from unittest import mock

from keystoneauth1 import adapter
from keystoneauth1 import session as ks_session

from nectarallocationclient import client

from nectarallocationclient.tests.unit import utils


ENDPOINT = 'http://allocations.example.com'


class SessionClientTest(utils.TestCase):
    def setUp(self):
        super().setUp()
        self.session = ks_session.Session()
        self.client = client.SessionClient(
            self.session, endpoint_override=ENDPOINT
        )
        patcher = mock.patch.object(
            client.SessionClient, 'get_project_id', return_value='fake-project'
        )
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_response_cookie_is_not_stored(self):
        self.requests_mock.get(
            f'{ENDPOINT}/allocations/',
            json={'results': []},
            cookies={'sessionid': 'abc123'},
        )

        self.client.get('/allocations/')

        self.assertEqual({}, dict(self.session.session.cookies))

    def test_cookie_is_not_carried_to_the_next_request(self):
        # The allocations API hands out a Django session cookie on every
        # authenticated call.  Keeping it would take over authentication
        # from the token on every later request.
        self.requests_mock.get(
            f'{ENDPOINT}/allocations/',
            json={'results': []},
            cookies={'sessionid': 'abc123'},
        )

        self.client.get('/allocations/')
        self.client.get('/allocations/')

        self.assertNotIn('Cookie', self.requests_mock.last_request.headers)

    def test_existing_cookies_are_cleared(self):
        session = ks_session.Session()
        session.session.cookies.set('sessionid', 'abc123')

        client.SessionClient(session, endpoint_override=ENDPOINT)

        self.assertEqual({}, dict(session.session.cookies))

    def test_disable_cookies_unwraps_an_adapter(self):
        session = ks_session.Session()
        session.session.cookies.set('sessionid', 'abc123')

        client.disable_cookies(adapter.Adapter(session=session))

        self.assertEqual({}, dict(session.session.cookies))
