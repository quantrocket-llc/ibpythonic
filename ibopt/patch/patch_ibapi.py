
import threading
import pkgutil
import ibapi
from ibapi.connection import Connection
from ibapi import connection, client

class FakeLock(object):
    """
    This is a dummy lock to disable locking of the IB socket connection, which
    is slow and unnecessary. https://github.com/InteractiveBrokers/tws-api/issues/464
    """
    def acquire(self):
        pass

    def release(self):
        pass

class NonlockingConnection(Connection):
    def __init__(self, *args, **kwargs):
        super(NonlockingConnection, self).__init__(*args, **kwargs)
        if hasattr(self, "lock"):
            self.lock = FakeLock()

def noop(*args, **kwargs):
    """
    Do nothing.
    """
    return

def silence_ibapi_logging():
    """
    Silences the excessive ibapi logging to the root logger.
    """
    for _, module_name, _ in pkgutil.iter_modules(ibapi.__path__):
        module = __import__("ibapi.{0}".format(module_name), fromlist="ibapi")
        if not hasattr(module, "logging"):
            continue
        module.logging.debug = module.logging.info = module.logging.error = noop

class PatchInstaller(object):
    """
    Patch installer which uses the Borg pattern to only run once.
    """

    __state = {} # Borg pattern

    def __init__(self):
        self.__dict__ = self.__state
        self.installed = getattr(self, 'installed', False)

    def __call__(self):
        """
        Disables locking and logging in ibapi.
        """
        if self.installed:
            return

        connection.Connection = NonlockingConnection
        client.Connection = NonlockingConnection
        silence_ibapi_logging()

        self.installed = True

patch = PatchInstaller()
