#!/usr/bin/env python
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'requests',
    ]

setup(
    name='Cloudpassage',
    version='0.0.1',
    author='Kevin C. Glisson',
    license='LICENSE.txt',
    description='Wrapper for Cloudpassage REST API',
    long_description=open('README.md').read(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='cloudpassage',
    install_requires=requires
)
