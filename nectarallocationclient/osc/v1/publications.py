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


class ListPublications(command.Lister):
    """List publications for an allocation."""

    log = logging.getLogger(__name__ + '.ListPublications')

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
        publications = client.publications.list(allocation=allocation.id)
        columns = ['id', 'output_type', 'publication', 'doi']
        return (
            columns,
            (osc_utils.get_item_properties(p, columns) for p in publications),
        )


class ShowPublication(command.ShowOne):
    """Show publication details."""

    log = logging.getLogger(__name__ + '.ShowPublication')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', metavar='<id>', help=('ID of publication'))
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        try:
            publication = client.publications.get(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        return self.dict2columns(publication.to_dict())


class CreatePublication(command.ShowOne):
    """Create a publication."""

    log = logging.getLogger(__name__ + '.CreatePublication')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'allocation',
            metavar='<allocation>',
            help=('ID or Name of allocation'),
        )
        parser.add_argument(
            '--output-type',
            metavar='<output_type>',
            required=True,
            choices=[
                'AJ',
                'AP',
                'AN',
                'B',
                'M',
                'D',
                'S',
                'P',
                'O',
                'U',
            ],
            help='Research output type: AJ (peer reviewed journal article), '
            'AP (other peer reviewed paper), AN (non-peer reviewed paper), '
            'B (book or book chapter), M (media publication), D (dataset), '
            'S (software), P (patent), O (other), U (unspecified)',
        )
        parser.add_argument(
            '--reference',
            metavar='<reference>',
            dest='publication',
            default='',
            help='Details of the research output (citation, title, URL, etc.)',
        )
        parser.add_argument(
            '--doi',
            metavar='<doi>',
            default='',
            help='Digital Object Identifier (required for journal articles)',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        allocation = get_allocation(client, parsed_args.allocation)
        publication = client.publications.create(
            allocation=allocation.id,
            output_type=parsed_args.output_type,
            publication=parsed_args.publication,
            doi=parsed_args.doi,
        )
        return self.dict2columns(publication.to_dict())


class DeletePublication(command.Command):
    """Delete a publication."""

    log = logging.getLogger(__name__ + '.DeletePublication')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', metavar='<id>', help=('ID of publication'))
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        client.publications.delete(parsed_args.id)
