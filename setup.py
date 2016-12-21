#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: python273
@contact: https://python273.pw/
@license: MIT License, see LICENSE file

Copyright (C) 2016
"""

from distutils.core import setup


setup(
    name='telegraph',
    version='1.1',
    author='python273',
    author_email='whoami@python273.pw',
    url='https://github.com/python273/telegraph',
    description='Telegraph API wrapper',
    download_url='https://github.com/python273/telegraph/archive/master.zip',
    license='MIT License, see LICENSE file',

    packages=['telegraph'],
    install_requires=['requests'],

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
