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
import re

from osc_lib.command import command
from osc_lib import utils as osc_utils

from nectarallocationclient import exceptions


def get_organisation(client, arg):
    if re.match(r'^\d+$', arg):
        try:
            return client.organisations.get(arg)
        except exceptions.NotFound:
            raise exceptions.CommandError(
                "Organisation with id '%s' not found" % arg)
    elif re.match(r'^https?://ror\.org/.+$', arg):
        filters = [{'ror_id__iexact': arg}]
    else:
        filters = [{'full_name__iexact': arg},
                   {'short_name__iexact': arg}]
    for f in filters:
        orgs = client.organisations.list(**f)
        if len(orgs) == 1:
            return orgs[0]
        elif len(orgs) > 0:
            raise exceptions.CommandError(
                "'%s' matches more than one organisation" % arg)
    raise exceptions.CommandError(
        "No organisation matches for '%s'" % arg)


def show_organisation(cmd, organisation):
    organisation_dict = organisation.to_dict()
    return cmd.dict2columns(organisation_dict)


class ListOrganisations(command.Lister):
    """List Organisations."""

    log = logging.getLogger(__name__ + '.ListOrganisations')

    def get_parser(self, prog_name):
        parser = super(ListOrganisations, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        orgs = client.organisations.list()
        columns = ['id', 'ror_id', 'full_name', 'short_name', 'country']
        return (
            columns,
            (osc_utils.get_item_properties(o, columns) for o in orgs)
        )


class ShowOrganisation(command.ShowOne):
    """Show Organisation details."""

    log = logging.getLogger(__name__ + '.ShowOrganisation')

    def get_parser(self, prog_name):
        parser = super(ShowOrganisation, self).get_parser(prog_name)
        parser.add_argument(
            'organisation',
            metavar='<organisation>',
            help=('ID, ror_id or name of organisation')
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        try:
            org = get_organisation(client, parsed_args.organisation)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        return show_organisation(self, org)


class ApproveOrganisation(command.Command):
    """Approve (vet) proposed organisation"""

    log = logging.getLogger(__name__ + '.ApproveOrganisation')

    def get_parser(self, prog_name):
        parser = super(ApproveOrganisation, self).get_parser(prog_name)
        parser.add_argument(
            'organisation',
            metavar='<organisation>',
            help=('ID, ror_id or name of organisation')
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        org = get_organisation(client, parsed_args.organisation)
        client.organisations.approve(org)


class DeclineOrganisation(command.Command):
    """Decline (vet) proposed organisation"""

    log = logging.getLogger(__name__ + '.DeclineOrganisation')

    def get_parser(self, prog_name):
        parser = super(DeclineOrganisation, self).get_parser(prog_name)
        parser.add_argument(
            'organisation',
            metavar='<organisation>',
            help=('ID, ror_id or name of of organisation')
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        org = get_organisation(client, parsed_args.organisation)
        client.organisations.decline(org)


class CreateOrganisation(command.ShowOne):
    """Create an Organisation."""

    log = logging.getLogger(__name__ + '.CreateOrganisationation')

    def get_parser(self, prog_name):
        parser = super(CreateOrganisation, self).get_parser(prog_name)
        parser.add_argument(
            'short_name',
            metavar='<short_name>',
            help='Short name of the organisation'
        )
        parser.add_argument(
            'full_name',
            metavar='<full_name>',
            help='Full name of the organisation'
        )
        parser.add_argument(
            'ror_id',
            metavar='<ror_id>',
            help='ROR id (URL) for the organisation'
        )
        parser.add_argument(
            'url',
            metavar='<url>',
            help='URL for the (local) organisation'
        )
        parser.add_argument(
            'country',
            metavar='<country>',
            help='Two letter country code for the organisation'
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)

        client = self.app.client_manager.allocation
        fields = {
            'full_name': parsed_args.full_name,
            'short_name': parsed_args.short_name,
            'ror_id': parsed_args.ror_id,
            'country': parsed_args.country,
            'url': parsed_args.url,
        }

        org = client.organisations.create(**fields)
        return show_organisation(self, org)
