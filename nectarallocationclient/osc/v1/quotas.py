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

from nectarallocationclient.osc.v1.allocations import get_allocation


class ListQuotas(command.Lister):

    log = logging.getLogger(__name__ + '.ListQuota')

    def get_parser(self, prog_name):
        parser = super(ListQuotas, self).get_parser(prog_name)
        parser.add_argument(
            'allocation',
            metavar='<allocation>',
            help=('ID or Name of allocation to display details for')
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
            if hasattr(resource, 'resource_type') and \
               resource.resource_type == 'boolean':
                q.quota = 'Enabled'
                q.unit = 'N/A'
        columns = ['zone', 'service', 'resource', 'quota', 'unit']
        return (
            columns,
            (osc_utils.get_item_properties(q, columns) for q in quotas)
        )
