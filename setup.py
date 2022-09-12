#!/usr/bin/env python

import setuptools

from pbr.packaging import parse_requirements


entry_points = {
    'openstack.cli.extension':
    ['allocation = nectarallocationclient.osc.plugin',],
    'openstack.allocation.v1':
    [
        'allocation list = nectarallocationclient.osc.v1.allocations:ListAllocations',
        'allocation show = nectarallocationclient.osc.v1.allocations:ShowAllocation',
        'allocation amend = nectarallocationclient.osc.v1.allocations:AmendAllocation',
        'allocation approve = nectarallocationclient.osc.v1.allocations:ApproveAllocation',
        'allocation delete = nectarallocationclient.osc.v1.allocations:DeleteAllocation',
        'allocation history = nectarallocationclient.osc.v1.allocations:AllocationHistory',
        'allocation create = nectarallocationclient.osc.v1.allocations:CreateAllocation',
        'allocation set = nectarallocationclient.osc.v1.allocations:UpdateAllocation',
        'allocation zone list = nectarallocationclient.osc.v1.zones:ListZones',
        'allocation zone show = nectarallocationclient.osc.v1.zones:ShowZone',
        'allocation zone compute-homes = nectarallocationclient.osc.v1.zones:ListComputeHomes',
        'allocation service-type list = nectarallocationclient.osc.v1.service_types:ListServiceTypes',
        'allocation service-type show = nectarallocationclient.osc.v1.service_types:ShowServiceType',
        'allocation quota list = nectarallocationclient.osc.v1.quotas:ListQuotas',
        'allocation quota history = nectarallocationclient.osc.v1.quotas:QuotaHistory',
        'allocation resource list = nectarallocationclient.osc.v1.resources:ListResources',
        'allocation resource show = nectarallocationclient.osc.v1.resources:ShowResource',
        'allocation grant list = nectarallocationclient.osc.v1.grants:ListGrants',
        'allocation grant show = nectarallocationclient.osc.v1.grants:ShowGrant',
        'allocation site list = nectarallocationclient.osc.v1.sites:ListSites',
        'allocation site show = nectarallocationclient.osc.v1.sites:ShowSite',
        'allocation facility list = nectarallocationclient.osc.v1.facilities:ListFacilities',
        'allocation facility show = nectarallocationclient.osc.v1.facilities:ShowFacility',
    ]
}


setuptools.setup(
    name='nectarallocationclient',
    version='1.8.0',
    description=('Client for the Nectar Allocation system'),
    author='Sam Morrison',
    author_email='sorrison@gmail.com',
    url='https://github.com/NeCTAR-RC/python-nectarallocationclient',
    packages=[
        'nectarallocationclient',
    ],
    include_package_data=True,
    install_requires=parse_requirements(),
    license="Apache",
    zip_safe=False,
    classifiers=(
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
    ),
    entry_points=entry_points,
)
