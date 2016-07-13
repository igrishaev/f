#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


setup(
    name = 'f',
    version = 123,
    description = "test",
    long_description = "test",
    author='Ivan Grishaev',
    author_email='test@test.com',
    url='todo',
    packages=['f'],
    # package_data={'': ['LICENSE', 'README.rst', 'HISTORY.rst']},
    include_package_data=True,
    install_requires=[],
    # license=open('LICENSE').read(),
    zip_safe=False,
    classifiers=(
    ),
)
