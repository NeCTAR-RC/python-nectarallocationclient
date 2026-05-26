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


class ShowResource(command.ShowOne):
    """Show resource details."""

    log = logging.getLogger(__name__ + '.ShowResource')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'resource_id',
            metavar='<resource_id>',
            help=('ID of resource to display details for'),
        )

        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)

        client = self.app.client_manager.allocation

        try:
            resource = client.resources.get(parsed_args.resource_id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        return self.dict2columns(resource.to_dict())


class ListResources(command.Lister):
    """List resource resources."""

    log = logging.getLogger(__name__ + '.ListResources')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)

        client = self.app.client_manager.allocation
        resources = client.resources.list()

        columns = [
            'id',
            'service_type',
            'name',
            'quota_name',
            'unit',
            'requestable',
            'resource_type',
        ]

        return (
            columns,
            (utils.get_item_properties(r, columns) for r in resources),
        )


class CreateResource(command.ShowOne):
    """Create a resource."""

    log = logging.getLogger(__name__ + '.CreateResource')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'name', metavar='<name>', help='Name of the resource'
        )
        parser.add_argument(
            'service_type',
            metavar='<service_type>',
            help='Service type catalog name',
        )
        parser.add_argument(
            'quota_name', metavar='<quota_name>', help='Quota name'
        )
        parser.add_argument('unit', metavar='<unit>', help='Unit')
        parser.add_argument(
            '--resource-type',
            metavar='<resource_type>',
            default='integer',
            choices=['integer', 'boolean'],
            help='Resource type (default: integer)',
        )
        parser.add_argument(
            '--not-requestable',
            action='store_true',
            help='Resource is not directly requestable',
        )
        parser.add_argument(
            '--help-text', metavar='<help_text>', default='', help='Help text'
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        resource = client.resources.create(
            name=parsed_args.name,
            service_type=parsed_args.service_type,
            quota_name=parsed_args.quota_name,
            unit=parsed_args.unit,
            requestable=not parsed_args.not_requestable,
            resource_type=parsed_args.resource_type,
            help_text=parsed_args.help_text,
        )
        return self.dict2columns(resource.to_dict())


class SetResource(command.ShowOne):
    """Update a resource."""

    log = logging.getLogger(__name__ + '.SetResource')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'resource_id', metavar='<resource_id>', help=('ID of resource')
        )
        parser.add_argument(
            '--property',
            metavar='<key=value>',
            action='append',
            help=(
                'Property to set on the resource. This can be '
                'specified multiple times'
            ),
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        fields = osc_utils.format_parameters(parsed_args.property)
        resource = client.resources.update(parsed_args.resource_id, **fields)
        return self.dict2columns(resource.to_dict())
