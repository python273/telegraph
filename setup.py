#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: python273
@contact: https://python273.pw/
@license: MIT License, see LICENSE file

Copyright (C) 2018
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = '2.2.0'


with open('README.md') as f:
    long_description = f.read()


setup(
    name='telegraph',
    version=version,

    author='python273',

    author_email='telegraph@python273.pw',
    url='https://github.com/python273/telegraph',

    description='Telegraph API wrapper',
    long_description=long_description,
    long_description_content_type='text/markdown',

    download_url='https://github.com/python273/telegraph/archive/v{}.zip'.format(
        version
    ),
    license='MIT',

    packages=['telegraph'],
    install_requires=['requests'],
    extras_require={
        'aio': ['httpx'],
    },

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ]
)
