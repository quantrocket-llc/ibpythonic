#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial, wraps

from ibapi.ticktype import TickTypeEnum


##
# To programmatically generate the TickTypeEnum filters, use something like this sketch:
#
# vs = [(name, value) for name, value in [(name, getattr(TickTypeEnum, name))
#                                         for name in dir(TickTypeEnum)] if type(value)==int]
# titlevalues = [(title[0].lower()+title[1:], value)
#                for title in [''.join([part.title() for part in name.split('_')])
#                              for name, value in vs]]


def messageFilter(function, predicate=lambda msg:True):
    @wraps(function)
    def inner(msg):
        if predicate(msg):
            return function(msg)
    return inner


askSizeFilter = partial(messageFilter, predicate=lambda msg:msg.field==TickTypeEnum.ASK_SIZE)
askPriceFilter = partial(messageFilter, predicate=lambda msg:msg.field==TickTypeEnum.ASK)

bidSizeFilter = partial(messageFilter, predicate=lambda msg:msg.field==TickTypeEnum.BID_SIZE)
bidPriceFilter = partial(messageFilter, predicate=lambda msg:msg.field==TickTypeEnum.BID)

lastSizeFilter = partial(messageFilter, predicate=lambda msg:msg.field==TickTypeEnum.LAST_SIZE)
lastPriceFilter = partial(messageFilter, predicate=lambda msg:msg.field==TickTypeEnum.LAST)


# We don't need functions for filtering by message type because that's
# what the reader/receiver/dispatcher already does.


class TickType:

    @classmethod
    def getField(cls, tickType):
        for tick_type_name in TickTypeEnum.idx2name.values():
            if tickType == getattr(TickTypeEnum, tick_type_name):
                return tick_type_name

        raise ValueError("unknown tickType: {0}".format(tickType))
