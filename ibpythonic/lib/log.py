from functools import wraps
import logging
import traceback

def logThreadErrors(target, logger):
    """
    Decorator that logs exceptions in the wrapped function.
    """
    @wraps(target)
    def wrapped(*args, **kwargs):
        try:
            target(*args, **kwargs)
        except Exception as e:
            tb = traceback.format_exc()
            lines = tb.split("\n")
            for l in lines:
                logger.error(l)
            raise

    return wrapped