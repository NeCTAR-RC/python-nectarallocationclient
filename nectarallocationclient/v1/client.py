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

from nectarallocationclient import client
from nectarallocationclient import exceptions
from nectarallocationclient.v1 import allocations
from nectarallocationclient.v1 import chiefinvestigators
from nectarallocationclient.v1 import facilities
from nectarallocationclient.v1 import grants
from nectarallocationclient.v1 import institutions
from nectarallocationclient.v1 import publications
from nectarallocationclient.v1 import quotas
from nectarallocationclient.v1 import resources
from nectarallocationclient.v1 import service_types
from nectarallocationclient.v1 import sites
from nectarallocationclient.v1 import zones


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
        self.chiefinvestigators = \
                chiefinvestigators.ChiefInvestigatorManager(self.http_client)
        self.facilities = facilities.FacilityManager(self.http_client)
        self.grants = grants.GrantManager(self.http_client)
        self.institutions = institutions.InstitutionManager(self.http_client)
        self.publications = publications.PublicationManager(self.http_client)
        self.quotas = quotas.QuotaManager(self.http_client)
        self.resources = resources.ResourceManager(self.http_client)
        self.service_types = service_types.ServiceTypeManager(self.http_client)
        self.sites = sites.SiteManager(self.http_client)
        self.zones = zones.ZoneManager(self.http_client)
