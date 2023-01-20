#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Defines Dispatcher class to send messages to registered listeners.
#
##
import logging
import traceback
from ibpythonic.lib import maybeName
from ibpythonic import message


class Dispatcher(object):
    """

    """
    def __init__(self, listeners=None, messageTypes=None, logger=None):
        """ Initializer.

        @param listeners=None mapping of existing listeners
        @param types=None method name to message type lookup
        """
        self.listeners = listeners if listeners else {}
        self.messageTypes = messageTypes if messageTypes else message.registry
        self.logger = logger or logging.getLogger("ibpythonic")

    def __call__(self, name, args):
        """ Send message to each listener.

        @param name method name
        @param args arguments for message instance
        @return None
        """
        results = []
        try:
            messageType = self.messageTypes[name]
            listeners = self.listeners[maybeName(messageType[0])]
        except (KeyError, ):
            return results
        message = messageType[0](**args)
        for listener in listeners:
            try:
                results.append(listener(message))
            except (Exception, ):
                errmsg = ("Exception in message dispatch.  "
                          f"Handler '{maybeName(listener)}' for '{name}'")
                self.logger.error(errmsg)
                tb = traceback.format_exc()
                lines = tb.split("\n")
                for l in lines:
                    self.logger.error(l)
                results.append(None)
        return results

    def enableLogging(self, enable=True):
        """ Enable or disable logging of all messages.

        @param enable if True (default), enables logging; otherwise disables
        @return True if enabled, False otherwise
        """
        if enable:
            self.registerAll(self.logMessage)
        else:
            self.unregisterAll(self.logMessage)
        return enable

    def logMessage(self, message):
        """ Format and send a message values to the logger.

        @param message instance of Message
        @return None
        """
        line = str.join(', ', ('%s=%s' % item for item in list(message.items())))
        self.logger.debug('%s(%s)', message.typeName, line)

    def register(self, listener, *types):
        """ Associate listener with message types created by this Dispatcher.

        @param listener callable to receive messages
        @param *types zero or more message types to associate with listener
        @return True if associated with one or more handler; otherwise False
        """
        count = 0
        for messagetype in types:
            key = maybeName(messagetype)
            listeners = self.listeners.setdefault(key, [])
            if listener not in listeners:
                listeners.append(listener)
                count += 1
        return count > 0

    def registerAll(self, listener):
        """ Associate listener with all messages created by this Dispatcher.

        @param listener callable to receive messages
        @return True if associated with one or more handler; otherwise False
        """
        return self.register(listener, *[maybeName(i) for v in list(self.messageTypes.values()) for i in v])

    def unregister(self, listener, *types):
        """ Disassociate listener with message types created by this Dispatcher.

        @param listener callable to no longer receive messages
        @param *types zero or more message types to disassociate with listener
        @return True if disassociated with one or more handler; otherwise False
        """
        count = 0
        for messagetype in types:
            try:
                listeners = self.listeners[maybeName(messagetype)]
            except (KeyError, ):
                pass
            else:
                if listener in listeners:
                    listeners.remove(listener)
                    count += 1
        return count > 0

    def unregisterAll(self, listener):
        """ Disassociate listener with all messages created by this Dispatcher.

        @param listener callable to no longer receive messages
        @return True if disassociated with one or more handler; otherwise False
        """
        return self.unregister(listener, *[maybeName(i) for v in list(self.messageTypes.values()) for i in v])
