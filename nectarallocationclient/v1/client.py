from nectarallocationclient import client
from nectarallocationclient import exceptions
from nectarallocationclient.v1 import allocations


class Client(object):
    """Client for the Nectar Allocations v1 API
    :param string session: session
    :type session: :py:class:`keystoneauth.adapter.Adapter`
    """

    def __init__(self, session=None, service_type='allocations', **kwargs):
        """Initialize a new client for the Nectar Allocations v1 API."""
        if session is None:
            raise exceptions.ClientException(
                message='Session is required argument')
        self.http_client = client.SessionClient(
            session, service_type=service_type, **kwargs)
        self.allocations = allocations.AllocationManager(self.http_client)
