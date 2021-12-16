#!/usr/bin/python
from setuptools import setup, find_packages
from klaviyo import __version__
setup(
    name = 'klaviyo',
    version = __version__,
    packages = find_packages(),
    install_requires=[
        'requests >= 2.2.1',
        'simplejson >= 3.17.0',
    ],

    # metadata for upload to PyPI
    author = 'Klaviyo',
    author_email = 'developers@klaviyo.com',
    description = "Deprecated Klaviyo SDK",
    long_description = (
"""
Deprecation Notice: This package is set to be deprecated on 2023-01-01 and will not receive further updates. To continue receiving API and SDK improvements, we recommend switching over to following pip package: https://pypi.org/project/klaviyo-sdk/
"""
    ),
    license = 'MIT License',
    keywords = 'klaviyo',
    url = 'http://github.com/klaviyo/python-klaviyo',
)
