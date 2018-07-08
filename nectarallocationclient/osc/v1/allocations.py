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
from osc_lib import utils

from nectarallocationclient import exceptions


class ShowAllocation(command.ShowOne):
    """Show allocation details."""

    log = logging.getLogger(__name__ + '.ShowAllocation')

    def get_parser(self, prog_name):
        parser = super(ShowAllocation, self).get_parser(prog_name)
        parser.add_argument(
            'allocation',
            metavar='<allocation>',
            help=('ID of allocation to display details for')
        )

        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)

        client = self.app.client_manager.allocation

        try:
            allocation = client.allocations.get(parsed_args.allocation)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        allocation_dict = allocation.to_dict()
        # Don't display quotas in allocation show
        allocation_dict.pop('quotas')
        return self.dict2columns(allocation_dict)


class ListAllocations(command.Lister):
    """List allocations."""

    log = logging.getLogger(__name__ + '.ListAllocations')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)

        client = self.app.client_manager.allocation
        allocations = client.allocations.list()

        columns = ['id', 'parent_request', 'project_name',
                   'project_description', 'contact_email']

        return (
            columns,
            (utils.get_item_properties(r, columns) for r in allocations)
        )


class ListAllocationQuotas(command.Lister):
    """List allocation qoutas."""

    log = logging.getLogger(__name__ + '.ListAllocations')

    def get_parser(self, prog_name):
        parser = super(ListAllocationQuotas, self).get_parser(prog_name)
        parser.add_argument(
            'allocation',
            metavar='<allocation>',
            help=('ID of allocation to display quota for')
        )

        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)

        client = self.app.client_manager.allocation
        try:
            allocation = client.allocations.get(parsed_args.allocation)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        columns = ['zone', 'resource', 'quota']
        return (
            columns,
            (utils.get_item_properties(q, columns) for q in allocation.quotas)
        )
