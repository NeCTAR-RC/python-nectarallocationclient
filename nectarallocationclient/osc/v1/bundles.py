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
            (osc_utils.get_item_properties(s, columns) for s in bundles)
        )


class ShowBundleQuotas(command.Lister):
    """List quotas for a bundle."""

    log = logging.getLogger(__name__ + '.ShowBundleQuotas')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<id>',
            help=('ID of bundle')
        )
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
            (osc_utils.get_item_properties(s, columns) for s in bundle.quotas)
        )


class ShowBundle(command.ShowOne):
    """Show bundle details."""

    log = logging.getLogger(__name__ + '.ShowBundle')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<id>',
            help=('ID of bundle')
        )
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
