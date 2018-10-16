#!/usr/bin/python
from setuptools import setup, find_packages

setup(
    name = 'klaviyo',
    version = '2.0.0',
    packages = find_packages(),

    install_requires=[
        'requests >= 2.2.1',
    ],

    # metadata for upload to PyPI
    author = 'Klaviyo',
    author_email = 'support@klaviyo.com',
    description = "Python API for Klaviyo",
    long_description = (
"""
Klaviyo is a real-time service for understanding your customers by aggregating
all your customer data, identifying important groups of customers
and then taking action.

Find out more at http://www.klaviyo.com
"""
    ),
    license = 'MIT License',
    keywords = 'klaviyo',
    url = 'http://github.com/klaviyo/python-klaviyo',
)
