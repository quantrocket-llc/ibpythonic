#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
import versioneer

setup(
    name='ibopt',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='IbPy-like interface for the Interactive Brokers Python API',
    maintainer='QuantRocket LLC',
    maintainer_email='support@quantrocket.com',
    url='https://github.com/quantrocket-llc/ibopt',
    license='BSD License',
    packages=['ibopt', 'ibopt/lib'],
)
