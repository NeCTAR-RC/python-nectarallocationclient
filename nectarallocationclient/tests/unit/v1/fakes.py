#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import re

import mock
from six.moves.urllib import parse

from nectarallocationclient import client as base_client
from nectarallocationclient import exceptions
from nectarallocationclient.tests.unit import fakes
from nectarallocationclient.tests.unit import utils
from nectarallocationclient.v1 import allocations
from nectarallocationclient.v1 import client

# regex to compare callback to result of get_endpoint()
# checks version number (vX or vX.X where X is a number)
# and also checks if the id is on the end
ENDPOINT_RE = re.compile(
    r"^get_http:__nectarallocation_api:8774_v\d(_\d)?_\w{32}$")

# accepts formats like v2 or v2.1
ENDPOINT_TYPE_RE = re.compile(r"^v\d(\.\d)?$")

# accepts formats like v2 or v2_1
CALLBACK_RE = re.compile(r"^get_http:__nectarallocation_api:8774_v\d(_\d)?$")

generic_allocation = {
    "id": 123,
    "quotas": [],
    "status": "A",
    "submit_date": "2018-07-03",
    "modified_time": "2018-07-03T07:36:48Z",
    "project_name": "rest-test3",
    "project_description": "testing rest",
    "contact_email": "user@fake.org",
    "start_date": "2018-07-04",
    "end_date": "2018-08-04",
    "estimated_project_duration": 1,
    "convert_trial_project": False,
    "approver_email": "user@fake.org",
    "use_case": "test",
    "usage_patterns": "",
    "allocation_home": "uom",
    "geographic_requirements": "",
    "project_id": None,
    "estimated_number_users": 1,
    "field_of_research_1": None,
    "for_percentage_1": 100,
    "field_of_research_2": None,
    "for_percentage_2": 0,
    "field_of_research_3": None,
    "for_percentage_3": 0,
    "nectar_support": "",
    "ncris_support": "",
    "funding_national_percent": 100,
    "funding_node": None,
    "notes": "test",
    "provisioned": False,
    "parent_request": None}


class FakeClient(fakes.FakeClient, client.Client):

    def __init__(self, *args, **kwargs):
        client.Client.__init__(self, session=mock.Mock())
        self.http_client = FakeSessionClient(**kwargs)
        self.allocations = allocations.AllocationManager(self.http_client)


class FakeSessionClient(base_client.SessionClient):

    def __init__(self, *args, **kwargs):

        self.callstack = []
        self.visited = []
        self.auth = mock.Mock()
        self.session = mock.Mock()
        self.service_type = 'service_type'
        self.service_name = None
        self.endpoint_override = None
        self.interface = None
        self.region_name = None
        self.version = None
        self.auth.get_auth_ref.return_value.project_id = 'tenant_id'
        # determines which endpoint to return in get_endpoint()
        # NOTE(augustina): this is a hacky workaround, ultimately
        # we need to fix our whole mocking architecture (fixtures?)
        if 'endpoint_type' in kwargs:
            self.endpoint_type = kwargs['endpoint_type']
        else:
            self.endpoint_type = 'endpoint_type'
        self.logger = mock.MagicMock()

    def request(self, url, method, **kwargs):
        return self._cs_request(url, method, **kwargs)

    def _cs_request(self, url, method, **kwargs):
        # Check that certain things are called correctly
        if method in ['GET', 'DELETE']:
            assert 'data' not in kwargs
        elif method == 'PUT':
            assert 'data' in kwargs

        if url is not None:
            # Call the method
            args = parse.parse_qsl(parse.urlparse(url)[4])
            kwargs.update(args)
            munged_url = url.rsplit('?', 1)[0]
            munged_url = munged_url.strip('/').replace('/', '_')
            munged_url = munged_url.replace('.', '_')
            munged_url = munged_url.replace('-', '_')
            munged_url = munged_url.replace(' ', '_')
            munged_url = munged_url.replace('!', '_')
            munged_url = munged_url.replace('@', '_')
            munged_url = munged_url.replace('%20', '_')
            munged_url = munged_url.replace('%3A', '_')
            callback = "%s_%s" % (method.lower(), munged_url)

        if url is None or callback == "get_http:__nectarallocation_api:8774":
            # To get API version information, it is necessary to GET
            # a nectarallocation endpoint directly without "v2/<tenant-id>".
            callback = "get_versions"
        elif CALLBACK_RE.search(callback):
            callback = "get_current_version"
        elif ENDPOINT_RE.search(callback):
            # compare callback to result of get_endpoint()
            # NOTE(sdague): if we try to call a thing that doesn't
            # exist, just return a 404. This allows the stack to act
            # more like we'd expect when making REST calls.
            raise exceptions.NotFound('404')

        simulate_pagination_next_links = [
            'get_os_simple_tenant_usage',
            'get_os_simple_tenant_usage_tenant_id',
        ]
        if callback in simulate_pagination_next_links:
            while callback in self.visited:
                callback += '_next'

        if not hasattr(self, callback):
            raise AssertionError('Called unknown API method: %s %s, '
                                 'expected fakes method name: %s' %
                                 (method, url, callback))

        # Note the call
        self.visited.append(callback)
        self.callstack.append((method, url, kwargs.get('data'),
                               kwargs.get('params')))

        status, headers, data = getattr(self, callback)(**kwargs)

        r = utils.TestResponse({
            "status_code": status,
            "text": data,
            "headers": headers,
        })
        return r, data

    def get_allocations(self, **kw):
        params = kw.get('params')
        allocations = [
            {
                "id": 587,
                "quotas": [],
                "status": "A",
                "submit_date": "2018-07-03",
                "modified_time": "2018-07-03T07:36:48Z",
                "project_name": "rest-test3",
                "project_description": "testing rest",
                "contact_email": "user@fake.org",
                "start_date": "2018-07-04",
                "end_date": "2018-08-04",
                "estimated_project_duration": 1,
                "convert_trial_project": False,
                "approver_email": "user@fake.org",
                "use_case": "test",
                "usage_patterns": "",
                "allocation_home": "uom",
                "geographic_requirements": "",
                "project_id": "123",
                "estimated_number_users": 1,
                "field_of_research_1": None,
                "for_percentage_1": 100,
                "field_of_research_2": None,
                "for_percentage_2": 0,
                "field_of_research_3": None,
                "for_percentage_3": 0,
                "nectar_support": "",
                "ncris_support": "",
                "funding_national_percent": 100,
                "funding_node": None,
                "provisioned": False,
                "parent_request": None
            },
            {
                "id": 596,
                "quotas": [],
                "status": "X",
                "submit_date": "2018-07-03",
                "modified_time": "2018-07-03T07:35:58Z",
                "project_name": "rest-test3",
                "project_description": "testing rest",
                "contact_email": "user@fake.org",
                "start_date": "2018-07-04",
                "end_date": "2018-08-04",
                "estimated_project_duration": 1,
                "convert_trial_project": False,
                "approver_email": "user@fake.org",
                "use_case": "test",
                "usage_patterns": "",
                "allocation_home": "uom",
                "geographic_requirements": "",
                "project_id": "123",
                "estimated_number_users": 1,
                "field_of_research_1": None,
                "for_percentage_1": 100,
                "field_of_research_2": None,
                "for_percentage_2": 0,
                "field_of_research_3": None,
                "for_percentage_3": 0,
                "nectar_support": "",
                "ncris_support": "",
                "funding_national_percent": 100,
                "funding_node": None,
                "provisioned": False,
                "parent_request": 587
            },
            {
                "id": 581,
                "quotas": [],
                "status": "A",
                "submit_date": "2018-07-03",
                "modified_time": "2018-07-03T07:28:36Z",
                "project_name": "rest-test3",
                "project_description": "testing rest",
                "contact_email": "sorrison@gmail.com",
                "start_date": "2018-07-04",
                "end_date": "2018-08-04",
                "estimated_project_duration": 1,
                "convert_trial_project": False,
                "approver_email": "sorrison@gmail.com",
                "use_case": "test",
                "usage_patterns": "",
                "allocation_home": "uom",
                "geographic_requirements": "",
                "project_id": "456",
                "estimated_number_users": 1,
                "field_of_research_1": None,
                "for_percentage_1": 100,
                "field_of_research_2": None,
                "for_percentage_2": 0,
                "field_of_research_3": None,
                "for_percentage_3": 0,
                "nectar_support": "",
                "ncris_support": "",
                "funding_national_percent": 100,
                "funding_node": None,
                "provisioned": False,
                "parent_request": None
            }
        ]
        no_parent = params.get('parent_request__isnull')
        project_id = params.get('project_id')
        if project_id:
            allocations = [a for a in allocations
                           if a['project_id'] == project_id]
        if no_parent:
            allocations = [a for a in allocations
                           if a['parent_request'] is None]

        return (200, {}, allocations)

    def get_allocations_123(self, **kw):
        return (200, {},
                {"id": 123,
                 "quotas": [],
                 "status": "A",
                 "submit_date": "2018-07-03",
                 "modified_time": "2018-07-03T07:36:48Z",
                 "project_name": "rest-test3",
                 "project_description": "testing rest",
                 "contact_email": "user@fake.org",
                 "start_date": "2018-07-04",
                 "end_date": "2018-08-04",
                 "estimated_project_duration": 1,
                 "convert_trial_project": False,
                 "approver_email": "user@fake.org",
                 "use_case": "test",
                 "usage_patterns": "",
                 "allocation_home": "uom",
                 "geographic_requirements": "",
                 "project_id": None,
                 "estimated_number_users": 1,
                 "field_of_research_1": None,
                 "for_percentage_1": 100,
                 "field_of_research_2": None,
                 "for_percentage_2": 0,
                 "field_of_research_3": None,
                 "for_percentage_3": 0,
                 "nectar_support": "",
                 "ncris_support": "",
                 "funding_national_percent": 100,
                 "funding_node": None,
                 "provisioned": False,
                 "parent_request": None
                })

    def patch_allocations_123(self, data, **kw):
        return (202, {'notes': 'test'},
                {"id": 123,
                 "quotas": [],
                 "status": "A",
                 "submit_date": "2018-07-03",
                 "modified_time": "2018-07-03T07:36:48Z",
                 "project_name": "rest-test3",
                 "project_description": "testing rest",
                 "contact_email": "user@fake.org",
                 "start_date": "2018-07-04",
                 "end_date": "2018-08-04",
                 "estimated_project_duration": 1,
                 "convert_trial_project": False,
                 "approver_email": "user@fake.org",
                 "use_case": "test",
                 "usage_patterns": "",
                 "allocation_home": "uom",
                 "geographic_requirements": "",
                 "project_id": None,
                 "estimated_number_users": 1,
                 "field_of_research_1": None,
                 "for_percentage_1": 100,
                 "field_of_research_2": None,
                 "for_percentage_2": 0,
                 "field_of_research_3": None,
                 "for_percentage_3": 0,
                 "nectar_support": "",
                 "ncris_support": "",
                 "funding_national_percent": 100,
                 "funding_node": None,
                 "notes": "test",
                 "provisioned": False,
                 "parent_request": None
                })

    def post_allocations_123_approve(self, **kw):
        return (202, {}, generic_allocation)

    def post_allocations_123_delete(self, **kw):
        return (202, {}, generic_allocation)

    def post_allocations_123_amend(self, **kw):
        return (202, {}, generic_allocation)
