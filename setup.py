#!/usr/bin/env python

import f

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='f',
    version=".".join(map(str, f.__version__)),
    description="Functional tools, collections and monads.",
    author=f.__author__,
    author_email=f.__email__,
    url="https://github.com/igrishaev/f",
    packages=['f'],
    include_package_data=True,
    install_requires=(
        'six==1.10.0',
    ),
    license=open('LICENSE').read(),
    zip_safe=False,
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ),
)
