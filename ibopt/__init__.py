#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# IbPy package root.
#
##

__version__ = '0.8.0'

from ibopt.patch.patch_ibapi import patch
patch()

##
# Sugary sweet layer of icing on top of the TWS API.
#
# Use:
#    {{{
#    from ibopt import ibConnection, message
#
#    def my_callback(msg):
#        ...
#
#    con = ibConnection()
#    con.register(my_callback, message.TickSize, message.TickPrice)
#    con.connect()
#    con.reqAccountUpdates(...)
#    ...
#    con.unregister(my_callback, message.TickSize)
#    }}}
#
# Enable and disable logging:
#
#    {{{
#    con.enableLogging()
#    ...
#    con.enableLogging(False)
#    }}}
##
from ibopt.connection import Connection


##
# This is the preferred client interface to this module.
# Alternatively, the Connection type can be sub-classed an its
# 'create' classmethod reused.
ibConnection = Connection.create
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
