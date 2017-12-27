# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sample',
    version='0.1.0',
    description='Python module for publishing Openstack metrics for Prometheus',
    long_description=readme,
    author='Rakesh Patnaik',
    author_email='patsrakesh@gmail.com',
    url='https://github.com/att-comdev/prometheus-openstack-exporter',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

