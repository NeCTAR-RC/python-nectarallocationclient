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


class ListSites(command.Lister):
    """List sites."""

    log = logging.getLogger(__name__ + '.ListSites')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        sites = client.sites.list()
        columns = ['id', 'name', 'display_name', 'enabled']
        return (
            columns,
            (osc_utils.get_item_properties(s, columns) for s in sites),
        )


class ShowSite(command.ShowOne):
    """Show site details."""

    log = logging.getLogger(__name__ + '.ShowSite')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', metavar='<id>', help=('ID of site'))
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        try:
            site = client.sites.get(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        return self.dict2columns(site.to_dict())


class CreateSite(command.ShowOne):
    """Create a site."""

    log = logging.getLogger(__name__ + '.CreateSite')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('name', metavar='<name>', help='Name of the site')
        parser.add_argument(
            'display_name',
            metavar='<display_name>',
            help='Display name of the site',
        )
        parser.add_argument(
            '--disabled',
            action='store_true',
            help='Create the site disabled (default: enabled)',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        site = client.sites.create(
            name=parsed_args.name,
            display_name=parsed_args.display_name,
            enabled=not parsed_args.disabled,
        )
        return self.dict2columns(site.to_dict())


class SetSite(command.ShowOne):
    """Update a site."""

    log = logging.getLogger(__name__ + '.SetSite')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', metavar='<id>', help=('ID of site'))
        parser.add_argument(
            '--property',
            metavar='<key=value>',
            action='append',
            help=(
                'Property to set on the site. This can be '
                'specified multiple times'
            ),
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        fields = utils.format_parameters(parsed_args.property)
        site = client.sites.update(parsed_args.id, **fields)
        return self.dict2columns(site.to_dict())
