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
from nectarallocationclient.osc import utils as osc_utils


class ShowZone(command.ShowOne):
    """Show zone details."""

    log = logging.getLogger(__name__ + '.ShowZone')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'zone',
            metavar='<zone>',
            help=('ID of zone to display details for'),
        )

        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)

        client = self.app.client_manager.allocation

        try:
            zone = client.zones.get(parsed_args.zone)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        return self.dict2columns(zone.to_dict())


class ListZones(command.Lister):
    """List zone resources."""

    log = logging.getLogger(__name__ + '.ListZones')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)

        client = self.app.client_manager.allocation
        zones = client.zones.list()

        columns = ['name', 'display_name']

        return (
            columns,
            (utils.get_item_properties(r, columns) for r in zones),
        )


class ListComputeHomes(command.Lister):
    """List zones available to a allocation home"""

    log = logging.getLogger(__name__ + '.ListComputeHomes')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)

        client = self.app.client_manager.allocation
        zones = client.zones.compute_homes()
        columns = ['Allocation Home', 'Zones']

        return (columns, zones.items())


class CreateZone(command.ShowOne):
    """Create a zone."""

    log = logging.getLogger(__name__ + '.CreateZone')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('name', metavar='<name>', help='Name of the zone')
        parser.add_argument(
            'display_name',
            metavar='<display_name>',
            help='Display name of the zone',
        )
        parser.add_argument(
            '--disabled',
            action='store_true',
            help='Create the zone disabled (default: enabled)',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        zone = client.zones.create(
            name=parsed_args.name,
            display_name=parsed_args.display_name,
            enabled=not parsed_args.disabled,
        )
        return self.dict2columns(zone.to_dict())


class SetZone(command.ShowOne):
    """Update a zone."""

    log = logging.getLogger(__name__ + '.SetZone')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('zone', metavar='<zone>', help=('ID of zone'))
        parser.add_argument(
            '--property',
            metavar='<key=value>',
            action='append',
            help=(
                'Property to set on the zone. This can be '
                'specified multiple times'
            ),
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        fields = osc_utils.format_parameters(parsed_args.property)
        zone = client.zones.update(parsed_args.zone, **fields)
        return self.dict2columns(zone.to_dict())
