#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Defines Sender class to handle outbound requests.
#
# Sender instances defer failed attribute lookup to their
# EClient member objects.
#
##
from functools import wraps
import threading

from ibapi.client import EClient
from ibopt.lib import toTypeName
from ibopt.message import registry, clientMethods


class Sender(object):
    """ Encapsulates an EClient instance, and proxies attribute
        lookup to it.

    """
    client = None

    def __init__(self, dispatcher):
        """ Initializer.

        @param dispatcher message dispatcher instance
        """
        self.dispatcher = dispatcher
        self.clientMethodNames = [m[0] for m in clientMethods]
        self.decoderThread = None

    def connect(self, host, port, clientId, handler, clientType=EClient):
        """ Creates a TWS client socket and connects it.

        @param host name of host for connection; default is localhost
        @param port port number for connection; default is 7496
        @param clientId client identifier to send when connected
        @param handler object to receive reader messages
        @keyparam clientType=EClient callable producing socket client
        @return True if connected, False otherwise
        """
        def reconnect():
            self.client = client = clientType(handler)
            client.connect(host, port, clientId)
            return client.isConnected()
        self.reconnect = reconnect
        success = self.reconnect()
        if success and self.decoderThread is None:
            # Start EClient.run in a thread
            self.decoderThread = threading.Thread(target=self.client.run)
            self.decoderThread.start()
        return success

    def disconnect(self):
        """ Disconnects the client.

        @return True if disconnected, False otherwise
        """
        client = self.client
        if client and client.isConnected():
            client.disconnect()
            success = not client.isConnected()
            if success:
                self.decoderThread = None
            return success
        return False

    def __getattr__(self, name):
        """ x.__getattr__('name') <==> x.name

        @return named attribute from EClient object
        """
        try:
            value = getattr(self.client, name)
        except (AttributeError, ):
            raise
        return value
