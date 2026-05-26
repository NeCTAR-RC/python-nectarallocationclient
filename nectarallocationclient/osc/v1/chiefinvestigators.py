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
from nectarallocationclient.osc.v1.allocations import get_allocation


class ListChiefInvestigators(command.Lister):
    """List chief investigators for an allocation."""

    log = logging.getLogger(__name__ + '.ListChiefInvestigators')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'allocation',
            metavar='<allocation>',
            help=('ID or Name of allocation to display details for'),
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        allocation = get_allocation(client, parsed_args.allocation)
        investigators = client.chiefinvestigators.list(
            allocation=allocation.id
        )
        columns = [
            'id',
            'title',
            'given_name',
            'surname',
            'email',
            'primary_organisation',
        ]
        return (
            columns,
            (
                osc_utils.get_item_properties(ci, columns)
                for ci in investigators
            ),
        )


class ShowChiefInvestigator(command.ShowOne):
    """Show chief investigator details."""

    log = logging.getLogger(__name__ + '.ShowChiefInvestigator')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'id', metavar='<id>', help=('ID of chief investigator')
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        try:
            ci = client.chiefinvestigators.get(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        return self.dict2columns(ci.to_dict())


class CreateChiefInvestigator(command.ShowOne):
    """Create a chief investigator."""

    log = logging.getLogger(__name__ + '.CreateChiefInvestigator')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'allocation',
            metavar='<allocation>',
            help=('ID or Name of allocation'),
        )
        parser.add_argument(
            '--title', metavar='<title>', default='', help='Title'
        )
        parser.add_argument(
            '--given-name',
            metavar='<given_name>',
            required=True,
            help='Given name',
        )
        parser.add_argument(
            '--surname', metavar='<surname>', required=True, help='Surname'
        )
        parser.add_argument(
            '--email', metavar='<email>', required=True, help='Email address'
        )
        parser.add_argument(
            '--primary-organisation',
            metavar='<organisation>',
            required=True,
            help='Primary organisation',
        )
        parser.add_argument(
            '--additional-researchers',
            metavar='<researchers>',
            default='',
            help='Additional researchers',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        allocation = get_allocation(client, parsed_args.allocation)
        ci = client.chiefinvestigators.create(
            allocation=allocation.id,
            title=parsed_args.title,
            given_name=parsed_args.given_name,
            surname=parsed_args.surname,
            email=parsed_args.email,
            primary_organisation=parsed_args.primary_organisation,
            additional_researchers=parsed_args.additional_researchers,
        )
        return self.dict2columns(ci.to_dict())


class DeleteChiefInvestigator(command.Command):
    """Delete a chief investigator."""

    log = logging.getLogger(__name__ + '.DeleteChiefInvestigator')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'id', metavar='<id>', help=('ID of chief investigator')
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        client.chiefinvestigators.delete(parsed_args.id)


class SetChiefInvestigator(command.ShowOne):
    """Update a chief investigator."""

    log = logging.getLogger(__name__ + '.SetChiefInvestigator')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'id', metavar='<id>', help=('ID of chief investigator')
        )
        parser.add_argument(
            '--property',
            metavar='<key=value>',
            action='append',
            help=(
                'Property to set on the chief investigator. This can be '
                'specified multiple times'
            ),
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        fields = utils.format_parameters(parsed_args.property)
        ci = client.chiefinvestigators.update(parsed_args.id, **fields)
        return self.dict2columns(ci.to_dict())
