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


class ShowResource(command.ShowOne):
    """Show resource details."""

    log = logging.getLogger(__name__ + '.ShowResource')

    def get_parser(self, prog_name):
        parser = super(ShowResource, self).get_parser(prog_name)
        parser.add_argument(
            'resource_id',
            metavar='<resource_id>',
            help=('ID of resource to display details for')
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

        columns = ['id', 'service_type', 'name', 'quota_name', 'unit',
                   'requestable', 'resource_type']

        return (
            columns,
            (utils.get_item_properties(r, columns) for r in resources)
        )
