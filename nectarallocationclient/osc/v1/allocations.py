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


class AllocationShowOne(command.ShowOne):

    def get_parser(self, prog_name):
        parser = super(AllocationShowOne, self).get_parser(prog_name)
        parser.add_argument(
            'allocation',
            metavar='<allocation>',
            help=('ID of allocation to display details for')
        )
        return parser

    def _show_allocation(self, allocation):
        allocation_dict = allocation.to_dict()
        # Don't display quotas in allocation show
        allocation_dict.pop('quotas')
        return self.dict2columns(allocation_dict)


class ShowAllocation(AllocationShowOne):
    """Show allocation details."""

    log = logging.getLogger(__name__ + '.ShowAllocation')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        try:
            allocation = client.allocations.get(parsed_args.allocation)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))
        return self._show_allocation(allocation)


class ApproveAllocation(AllocationShowOne):
    """Approve allocation"""

    log = logging.getLogger(__name__ + '.ApproveAllocation')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        try:
            allocation = client.allocations.approve(parsed_args.allocation)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))
        return self._show_allocation(allocation)


class AmendAllocation(AllocationShowOne):
    """Amend allocation"""

    log = logging.getLogger(__name__ + '.AmendAllocation')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        try:
            allocation = client.allocations.amend(parsed_args.allocation)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))
        return self._show_allocation(allocation)


class ListAllocations(command.Lister):
    """List allocations."""

    log = logging.getLogger(__name__ + '.ListAllocations')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)

        client = self.app.client_manager.allocation
        allocations = client.allocations.list(parent_request__isnull=True)

        columns = ['id', 'project_name',
                   'contact_email', 'status_display']

        return (
            columns,
            (osc_utils.get_item_properties(r, columns) for r in allocations)
        )


class AllocationHistory(command.Lister):
    """List allocations."""

    log = logging.getLogger(__name__ + '.ListAllocations')

    def get_parser(self, prog_name):
        parser = super(AllocationHistory, self).get_parser(prog_name)
        parser.add_argument(
            'allocation',
            metavar='<allocation>',
            help=('ID of allocation to display history for')
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)

        client = self.app.client_manager.allocation

        try:
            allocation = client.allocations.get(parsed_args.allocation)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))
        allocations = client.allocations.list(
            parent_request=parsed_args.allocation)
        allocations.insert(0, allocation)
        columns = ['modified_time', 'status_display', 'start_date', 'end_date',
                   'contact_email']

        return (
            columns,
            (osc_utils.get_item_properties(r, columns) for r in allocations)
        )


class CreateAllocation(AllocationShowOne):
    """Create an allocation."""

    log = logging.getLogger(__name__ + '.CreateAllocation')

    def get_parser(self, prog_name):
        parser = super(AllocationShowOne, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Name of the allocation to create'
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            required=True,
            help='Description of the allocation to create'
        )
        parser.add_argument(
            '--home',
            metavar='<home>',
            required=True,
            help='Allocation home'
        )
        parser.add_argument(
            '--start-date',
            metavar='<YYYY-MM-DD>',
            required=True,
            help='Start date - YYYY-MM-DD'
        )
        parser.add_argument(
            '--use-case',
            metavar='<user-case>',
            required=True,
            help='Use case'
        )
        parser.add_argument(
            '--estimated-number-users',
            metavar='<users>',
            help='Estimated number of users',
            default=1,
            type=int,
        )
        parser.add_argument(
            '--estimated-duration',
            metavar='<months>',
            help='Estimated duration in months',
            default=6,
            type=int,
        )
        parser.add_argument(
            '--for-code-1',
            metavar='<FOR code>',
            help='Field Of Research Code 1',
            type=int,
        )
        parser.add_argument(
            '--for-code-2',
            metavar='<FOR code>',
            help='Field Of Research Code 2',
            type=int,
        )
        parser.add_argument(
            '--for-code-3',
            metavar='<FOR code>',
            help='Field Of Research Code 3',
            type=int,
        )
        parser.add_argument(
            '--for-percentage-1',
            metavar='<percent>',
            help='Field Of Research Code 1 percentage 1-100',
            default=0,
            type=int,
        )
        parser.add_argument(
            '--for-percentage-2',
            metavar='<percent>',
            help='Field Of Research Code 2 percentage 1-100',
            default=0,
            type=int,
        )
        parser.add_argument(
            '--for-percentage-3',
            metavar='<percent>',
            help='Field Of Research Code 3 percentage 1-100',
            default=0,
            type=int,
        )
        parser.add_argument(
            '--convert-trial-project',
            action='store_true',
            help='Convert Project Trial of user to this allocation'
        )
        parser.add_argument(
            '--geographic-requirements',
            metavar='<requirements>',
            help='Geographic requirements'
        )
        parser.add_argument(
            '--ncris-support',
            metavar='<details>',
            help='NCRIS Support'
        )
        parser.add_argument(
            '--nectar-support',
            metavar='<details>',
            help='Nectar support'
        )
        parser.add_argument(
            '--usage-pattterns',
            metavar='<details>',
            help='Usage pattterns'
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)

        client = self.app.client_manager.allocation
        fields = {
            'project_name': parsed_args.name,
            'project_description': parsed_args.description,
            'start_date': parsed_args.start_date,
            'convert_trial_project': parsed_args.convert_trial_project,
            'allocation_home': parsed_args.home,
            'use_case': parsed_args.use_case,
            'estimated_number_users': parsed_args.estimated_number_users,
            'estimated_project_duration': parsed_args.estimated_duration,
            'field_of_research_1': parsed_args.for_code_1,
            'field_of_research_2': parsed_args.for_code_2,
            'field_of_research_3': parsed_args.for_code_3,
            'for_percentage_1': parsed_args.for_percentage_1,
            'for_percentage_2': parsed_args.for_percentage_2,
            'for_percentage_3': parsed_args.for_percentage_3,
            'geographic_requirements': parsed_args.geographic_requirements,
            'ncris_support': parsed_args.ncris_support,
            'nectar_support': parsed_args.nectar_support,
            'usage_pattterns': parsed_args.usage_pattterns,
        }

        allocation = client.allocations.create(**fields)
        return self._show_allocation(allocation)


class UpdateAllocation(AllocationShowOne):
    """Update an allocation."""

    log = logging.getLogger(__name__ + '.UpdateAllocation')

    def get_parser(self, prog_name):
        parser = super(UpdateAllocation, self).get_parser(prog_name)
        parser.add_argument(
            '--property',
            metavar='<key=value>',
            action='append',
            help=('Properties to set on the allocation. This can be '
                  'specified multiple times'))
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)

        client = self.app.client_manager.allocation

        try:
            allocation = client.allocations.get(parsed_args.allocation)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        fields = utils.format_parameters(parsed_args.property)
        allocation = allocation.update(**fields)
        return self._show_allocation(allocation)
