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

from keystoneauth1 import adapter
from oslo_utils import importutils

from nectarallocationclient import exceptions


def Client(version, *args, **kwargs):
    module = 'nectarallocationclient.v%s.client' % version
    module = importutils.import_module(module)
    client_class = getattr(module, 'Client')
    return client_class(*args, **kwargs)


class SessionClient(adapter.Adapter):

    client_name = 'python-nectarallocationclient'
    client_version = '1.7.0'

    def request(self, url, method, **kwargs):
        project_id = self.get_project_id()
        kwargs.setdefault('headers', kwargs.get('headers', {}))
        kwargs['headers']['X-PROJECT-ID'] = project_id
        # NOTE(sorrison): The standard call raises errors from
        # keystoneauth, where we need to raise the nectarallocation errors.
        raise_exc = kwargs.pop('raise_exc', True)
        resp = super(SessionClient, self).request(url,
                                                  method,
                                                  raise_exc=False,
                                                  **kwargs)

        if raise_exc and resp.status_code >= 400:
            raise exceptions.from_response(resp, url, method)
        # NOTE(sorrison): Deletes don't return json body
        if resp.status_code == 204:
            return resp, '{}'
        return resp, resp.json()
