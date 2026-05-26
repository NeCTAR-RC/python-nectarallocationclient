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


class ListBundles(command.Lister):
    """List bundles."""

    log = logging.getLogger(__name__ + '.ListBundles')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        bundles = client.bundles.list()
        columns = ['id', 'name', 'su_per_year']
        return (
            columns,
            (osc_utils.get_item_properties(s, columns) for s in bundles),
        )


class ShowBundleQuotas(command.Lister):
    """List quotas for a bundle."""

    log = logging.getLogger(__name__ + '.ShowBundleQuotas')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', metavar='<id>', help=('ID of bundle'))
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        try:
            bundle = client.bundles.get(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        columns = ['resource', 'quota']
        return (
            columns,
            (osc_utils.get_item_properties(s, columns) for s in bundle.quotas),
        )


class ShowBundle(command.ShowOne):
    """Show bundle details."""

    log = logging.getLogger(__name__ + '.ShowBundle')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', metavar='<id>', help=('ID of bundle'))
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        try:
            bundle = client.bundles.get(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        bundle_dict = bundle.to_dict()
        # Don't display quotas in bundle show
        bundle_dict.pop('quotas')
        return self.dict2columns(bundle_dict)


class CreateBundle(command.ShowOne):
    """Create a bundle."""

    log = logging.getLogger(__name__ + '.CreateBundle')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'name', metavar='<name>', help='Name of the bundle'
        )
        parser.add_argument('zone', metavar='<zone>', help='Zone name')
        parser.add_argument(
            'order', metavar='<order>', type=int, help='Display order'
        )
        parser.add_argument(
            'su_per_year',
            metavar='<su_per_year>',
            type=int,
            help='SU budget per year',
        )
        parser.add_argument(
            '--description', metavar='<description>', default='', help='Desc'
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        bundle = client.bundles.create(
            name=parsed_args.name,
            description=parsed_args.description,
            zone=parsed_args.zone,
            order=parsed_args.order,
            su_per_year=parsed_args.su_per_year,
        )
        bundle_dict = bundle.to_dict()
        bundle_dict.pop('quotas', None)
        return self.dict2columns(bundle_dict)


class SetBundle(command.ShowOne):
    """Update a bundle."""

    log = logging.getLogger(__name__ + '.SetBundle')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', metavar='<id>', help=('ID of bundle'))
        parser.add_argument(
            '--property',
            metavar='<key=value>',
            action='append',
            help=(
                'Property to set on the bundle. This can be '
                'specified multiple times'
            ),
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        fields = utils.format_parameters(parsed_args.property)
        bundle = client.bundles.update(parsed_args.id, **fields)
        bundle_dict = bundle.to_dict()
        bundle_dict.pop('quotas', None)
        return self.dict2columns(bundle_dict)
