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
    client_version = '0.1'

    def request(self, url, method, **kwargs):
        kwargs.setdefault('headers', kwargs.get('headers', {}))
        # NOTE(sileht): The standard call raises errors from
        # keystoneauth, where we need to raise the nectarallocation errors.
        raise_exc = kwargs.pop('raise_exc', True)
        resp = super(SessionClient, self).request(url,
                                                  method,
                                                  raise_exc=False,
                                                  **kwargs)

        if raise_exc and resp.status_code >= 400:
            raise exceptions.from_response(resp, url, method)
        return resp, resp.json()
