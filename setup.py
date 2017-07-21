#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ibopt is an IbPy-like interface to the official Interactive Brokers Python API
"""
import os
import re
from distutils.core import setup


classifiers = """Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python
Topic :: Office/Business :: Financial
Topic :: Office/Business :: Financial :: Investment
Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator
Topic :: Software Development :: Libraries
Topic :: Software Development :: Libraries :: Python Modules"""


doclines = __doc__.split('\n')

# Version Number
with open(os.path.join(os.path.dirname(__file__), 'ibopt', '__init__.py')) as f:
    version = re.compile(r".*__version__ = '(.*?)'", re.S).match(f.read()).group(1)

setup(
    name='ibopt',
    version=version,
    description=doclines[0],
    maintainer='QuantRocket LLC',
    maintainer_email='support@quantrocket.com',
    url='https://github.com/quantrocket-llc/ibopt',
    license='BSD License',
    packages=['ibopt', 'ibopt/lib'],
    classifiers=classifiers.split('\n'),
    long_description='\n'.join(doclines[2:]),
    platforms=['any']
)
