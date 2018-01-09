import logging

from utils import emit

logger = logging.getLogger(__name__)

discovered_samples = {}


def resource(decorated_resource):
    def decorate(sample_func):
        def run(*args, **kwargs):
            emit("Running `{0}.{1}`".format(sample_func.__module__, sample_func.__name__))
            sample_func(*args, **kwargs)

        run.__name__ = sample_func.__name__

        if sample_func.__module__ not in discovered_samples:
            logger.debug("Discovered area `%s`", sample_func.__module__)
            discovered_samples[sample_func.__module__] = {}

        area_samples = discovered_samples[sample_func.__module__]
        if decorated_resource not in area_samples:
            logger.debug("Discovered resource `%s`", decorated_resource)
            area_samples[decorated_resource] = []

        logger.debug("Discovered function `%s`", sample_func.__name__)
        area_samples[decorated_resource].append(run)

        return run
    return decorate
