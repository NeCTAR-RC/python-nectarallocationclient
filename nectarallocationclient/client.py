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

from http import cookiejar

from keystoneauth1 import adapter
from oslo_utils import importutils

import nectarallocationclient
from nectarallocationclient import exceptions


def Client(version, *args, **kwargs):
    module = f'nectarallocationclient.v{version}.client'
    module = importutils.import_module(module)
    client_class = getattr(module, 'Client')
    return client_class(*args, **kwargs)


class BlockCookies(cookiejar.DefaultCookiePolicy):
    """A cookie policy that neither stores nor sends any cookie.

    requests merges a session's cookies into a fresh jar before sending, so
    only set_ok() is consulted in practice.  That is enough: a cookie that
    is never stored is never sent.
    """

    def set_ok(self, cookie, request):
        return False

    def return_ok(self, cookie, request):
        return False


def disable_cookies(session):
    """Stop a session holding on to cookies handed out by the API.

    The allocations API is a Django application, and authenticating to it
    creates a Django session and returns a sessionid cookie.  keystoneauth
    keeps cookies in its underlying requests.Session for the life of the
    process, and the API prefers its own session authentication over the
    token, so a client that hangs on to that cookie stops being
    authenticated by the token it sends.  Once the keystone token held
    inside that Django session expires, every subsequent request is
    silently downgraded to anonymous, and only restarting the process
    recovers.  Nothing here needs cookies, so drop them.
    """
    # A keystoneauth Session, or an Adapter wrapping one, was passed in.
    # The requests.Session that owns the cookie jar sits at the bottom of
    # that chain.
    for _ in range(3):
        if session is None:
            return
        if hasattr(session, 'cookies'):
            session.cookies.set_policy(BlockCookies())
            session.cookies.clear()
            return
        session = getattr(session, 'session', None)


class SessionClient(adapter.Adapter):
    client_name = 'python-nectarallocationclient'
    client_version = nectarallocationclient.__version__

    def __init__(self, session, **kwargs):
        super().__init__(session, **kwargs)
        disable_cookies(session)

    def request(self, url, method, **kwargs):
        project_id = self.get_project_id()
        kwargs.setdefault('headers', kwargs.get('headers', {}))
        kwargs['headers']['X-PROJECT-ID'] = project_id
        # NOTE(sorrison): The standard call raises errors from
        # keystoneauth, where we need to raise the nectarallocation errors.
        raise_exc = kwargs.pop('raise_exc', True)
        resp = super().request(url, method, raise_exc=False, **kwargs)

        if raise_exc and resp.status_code >= 400:
            raise exceptions.from_response(resp, url, method)
        # NOTE(sorrison): Deletes don't return json body
        if resp.status_code == 204:
            return resp, '{}'
        return resp, resp.json()
