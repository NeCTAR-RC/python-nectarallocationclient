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
from nectarallocationclient.osc.v1.allocations import get_allocation


class ListQuotas(command.Lister):
    log = logging.getLogger(__name__ + '.ListQuota')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'allocation',
            metavar='<allocation>',
            help=('ID or Name of allocation to display details for'),
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        allocation = get_allocation(client, parsed_args.allocation)
        quotas = client.quotas.list(allocation=allocation.id)
        for q in quotas:
            resource = client.resources.get(q.resource)
            q.resource = resource.name
            q.service = resource.service_type
            q.unit = resource.unit
            if (
                hasattr(resource, 'resource_type')
                and resource.resource_type == 'boolean'
            ):
                q.quota = 'Enabled'
                q.unit = 'N/A'
        columns = [
            'zone',
            'service',
            'resource',
            'requested_quota',
            'quota',
            'unit',
        ]
        return (
            columns,
            (osc_utils.get_item_properties(q, columns) for q in quotas),
        )


class QuotaHistory(command.Lister):
    """List quota history for an allocation and resource."""

    log = logging.getLogger(__name__ + '.QuotaHistory')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'allocation',
            metavar='<allocation>',
            help=('ID or Name of allocation to display history for'),
        )
        parser.add_argument(
            'resource_id', metavar='<resource_id>', help=('Resource ID')
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)

        client = self.app.client_manager.allocation
        allocation = get_allocation(client, parsed_args.allocation)
        resource = client.resources.get(parsed_args.resource_id)
        allocations = client.allocations.list(parent_request=allocation.id)
        allocations.insert(0, allocation)

        quota_history = []
        for allocation in allocations:
            quotas = client.quotas.list(
                allocation=allocation.id, resource=resource.id
            )
            if quotas:
                quotas[0].allocation_id = allocation.id
                quotas[0].modified_time = allocation.modified_time
                quota_history.append(quotas[0])
        columns = [
            'allocation_id',
            'modified_time',
            'requested_quota',
            'quota',
        ]

        return (
            columns,
            (osc_utils.get_item_properties(r, columns) for r in quota_history),
        )


class CreateQuota(command.ShowOne):
    """Create a quota for an allocation."""

    log = logging.getLogger(__name__ + '.CreateQuota')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'allocation',
            metavar='<allocation>',
            help=('ID or Name of allocation'),
        )
        parser.add_argument(
            'resource',
            metavar='<resource>',
            help='Resource ID',
        )
        parser.add_argument('zone', metavar='<zone>', help='Zone name')
        parser.add_argument(
            'quota', metavar='<quota>', type=int, help='Approved quota value'
        )
        parser.add_argument(
            '--requested-quota',
            metavar='<requested_quota>',
            type=int,
            help='Requested quota value (defaults to the approved quota)',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        allocation = get_allocation(client, parsed_args.allocation)
        quota = client.quotas.create(
            allocation=allocation.id,
            resource=parsed_args.resource,
            zone=parsed_args.zone,
            quota=parsed_args.quota,
            requested_quota=parsed_args.requested_quota,
        )
        return self.dict2columns(quota.to_dict())


class DeleteQuota(command.Command):
    """Delete a quota."""

    log = logging.getLogger(__name__ + '.DeleteQuota')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', metavar='<id>', help=('ID of quota'))
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.allocation
        try:
            client.quotas.delete(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))
