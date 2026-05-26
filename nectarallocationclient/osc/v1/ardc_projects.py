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


class ListARDCProjects(command.Lister):
    """List ARDC programs and projects."""

    log = logging.getLogger(__name__ + '.ListARDCProjects')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        projects = client.ardc_projects.list()
        columns = [
            'id',
            'short_name',
            'name',
            'project',
            'project_id',
            'enabled',
        ]
        return (
            columns,
            (osc_utils.get_item_properties(p, columns) for p in projects),
        )


class ShowARDCProject(command.ShowOne):
    """Show ARDC program or project details."""

    log = logging.getLogger(__name__ + '.ShowARDCProject')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', metavar='<id>', help=('ID of ARDC project'))
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        try:
            project = client.ardc_projects.get(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        return self.dict2columns(project.to_dict())


class CreateARDCProject(command.ShowOne):
    """Create an ARDC program or project."""

    log = logging.getLogger(__name__ + '.CreateARDCProject')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'short_name',
            metavar='<short_name>',
            help='Common short name or acronym',
        )
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Full ARDC program or project name',
        )
        parser.add_argument(
            '--program',
            action='store_true',
            help='Mark as a program rather than a project (default: project)',
        )
        parser.add_argument(
            '--project-id',
            metavar='<project_id>',
            default='',
            help='ARDC project ID',
        )
        parser.add_argument(
            '--rank',
            metavar='<rank>',
            type=int,
            default=100,
            help='Ranking in menus (smaller is earlier)',
        )
        parser.add_argument(
            '--explain',
            action='store_true',
            help='Require the user to provide support details',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        project = client.ardc_projects.create(
            name=parsed_args.name,
            short_name=parsed_args.short_name,
            project=not parsed_args.program,
            project_id=parsed_args.project_id,
            rank=parsed_args.rank,
            explain=parsed_args.explain,
        )
        return self.dict2columns(project.to_dict())


class SetARDCProject(command.ShowOne):
    """Update an ARDC program or project."""

    log = logging.getLogger(__name__ + '.SetARDCProject')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', metavar='<id>', help=('ID of ARDC project'))
        parser.add_argument(
            '--property',
            metavar='<key=value>',
            action='append',
            help=(
                'Property to set on the ARDC project. This can be '
                'specified multiple times'
            ),
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        fields = utils.format_parameters(parsed_args.property)
        project = client.ardc_projects.update(parsed_args.id, **fields)
        return self.dict2columns(project.to_dict())
