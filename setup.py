#!/usr/bin/env python3

from setuptools import setup

setup(
    name='NetworkSimulator',
    version='0.0',
    description='Network/Graph simulation package',
    author='Elias Malik',
    packages=['networksimulator'],
    install_requires=['networkx', 'simpy', 'numpy', 'scipy']
)
