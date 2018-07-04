#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

requirements = parse_requirements("requirements.txt", session=False)

setup(
    name='nectarallocationclient',
    version='0.1.0',
    description=('Client for the Nectar Allocation system'),
    author='Sam Morrison',
    author_email='sam@nectar.org.au',
    url='https://github.com/NeCTAR-RC/python-nectarallocationclient',
    packages=[
        'nectarallocationclient',
    ],
    include_package_data=True,
    install_requires=[str(r.req) for r in requirements],
    license="GPLv3+",
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        ('License :: OSI Approved :: '
         'GNU General Public License v3 or later (GPLv3+)'),
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)