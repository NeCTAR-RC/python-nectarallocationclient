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

import logging

from osc_lib.command import command
from osc_lib import utils as osc_utils

from nectarallocationclient import exceptions
from nectarallocationclient.osc.v1.allocations import get_allocation


class ListGrants(command.Lister):
    """List grants."""

    log = logging.getLogger(__name__ + '.ListGrants')

    def get_parser(self, prog_name):
        parser = super(ListGrants, self).get_parser(prog_name)
        parser.add_argument(
            'allocation',
            metavar='<allocation>',
            help=('ID or Name of allocation to display details for')
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        allocation = get_allocation(client, parsed_args.allocation)
        grants = client.grants.list(allocation=allocation.id)
        columns = ['id', 'grant_id', 'grant_type', 'funding_body_scheme',
                   'first_year_funded', 'last_year_funded', 'total_funding']
        return (
            columns,
            (osc_utils.get_item_properties(q, columns) for q in grants)
        )


class ShowGrant(command.ShowOne):
    """Show grant details."""

    log = logging.getLogger(__name__ + '.ShowGrant')

    def get_parser(self, prog_name):
        parser = super(ShowGrant, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<id>',
            help=('ID of grant')
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        try:
            grant = client.grants.get(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        return self.dict2columns(grant.to_dict())
