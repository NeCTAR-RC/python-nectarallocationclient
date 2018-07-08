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


class ShowServiceType(command.ShowOne):
    """Show service type details."""

    log = logging.getLogger(__name__ + '.ShowServiceType')

    def get_parser(self, prog_name):
        parser = super(ShowServiceType, self).get_parser(prog_name)
        parser.add_argument(
            'service_type',
            metavar='<service_type>',
            help=('ID of service_type to display details for')
        )

        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)

        client = self.app.client_manager.allocation

        try:
            service_type = client.service_types.get(parsed_args.service_type)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        return self.dict2columns(service_type.to_dict())


class ListServiceTypes(command.Lister):
    """List service type resources."""

    log = logging.getLogger(__name__ + '.ListServiceTypes')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)

        client = self.app.client_manager.allocation
        service_types = client.service_types.list()

        columns = ['catalog_name', 'name', 'zones']

        return (
            columns,
            (utils.get_item_properties(r, columns) for r in service_types)
        )
