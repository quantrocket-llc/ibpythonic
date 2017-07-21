#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from ibapi_grease import patch_all
except ImportError:
    pass
else:
    patch_all()

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
from ibopt.connection import Connection


##
# This is the preferred client interface to this module.
# Alternatively, the Connection type can be sub-classed an its
# 'create' classmethod reused.
ibConnection = Connection.create
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
