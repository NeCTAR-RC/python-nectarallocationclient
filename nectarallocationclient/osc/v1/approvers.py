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
from nectarallocationclient.osc import utils


class ListApprovers(command.Lister):
    """List approvers."""

    log = logging.getLogger(__name__ + '.ListApprovers')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        approvers = client.approvers.list()
        columns = ['id', 'username', 'display_name', 'sites']
        return (
            columns,
            (osc_utils.get_item_properties(a, columns) for a in approvers),
        )


class ShowApprover(command.ShowOne):
    """Show approver details."""

    log = logging.getLogger(__name__ + '.ShowApprover')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', metavar='<id>', help=('ID of approver'))
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        try:
            approver = client.approvers.get(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        return self.dict2columns(approver.to_dict())


class CreateApprover(command.ShowOne):
    """Create an approver."""

    log = logging.getLogger(__name__ + '.CreateApprover')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'username',
            metavar='<username>',
            help='Email address of the approver',
        )
        parser.add_argument(
            'display_name',
            metavar='<display_name>',
            help='Display name of the approver',
        )
        parser.add_argument(
            '--site',
            metavar='<site>',
            action='append',
            default=[],
            help='Site ID the approver is authorised for (repeat as required)',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        approver = client.approvers.create(
            username=parsed_args.username,
            display_name=parsed_args.display_name,
            sites=parsed_args.site,
        )
        return self.dict2columns(approver.to_dict())


class SetApprover(command.ShowOne):
    """Update an approver."""

    log = logging.getLogger(__name__ + '.SetApprover')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', metavar='<id>', help=('ID of approver'))
        parser.add_argument(
            '--property',
            metavar='<key=value>',
            action='append',
            help=(
                'Property to set on the approver. This can be '
                'specified multiple times'
            ),
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        fields = utils.format_parameters(parsed_args.property)
        approver = client.approvers.update(parsed_args.id, **fields)
        return self.dict2columns(approver.to_dict())
