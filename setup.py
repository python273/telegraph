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
    version='1.0',
    author='python273',
    author_email='whoami@python273.pw',
    url='https://github.com/python273/telegraph',
    description='Telegraph API wrapper',
    download_url='https://github.com/python273/telegraph/archive/master.zip',
    license='MIT License, see LICENSE file',

    packages=['telegraph'],
    install_requires=['requests']
)
