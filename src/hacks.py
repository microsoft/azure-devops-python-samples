import logging
import warnings

from http_logging import requests_hook


logger = logging.getLogger(__name__)


def add_request_hook(client):
    "This is a bit of a hack until we have a supported way to install the hook."
    warnings.warn("hacking in the request hook", DeprecationWarning)

    if requests_hook in client.config.hooks:
        logger.debug("hook already installed; skipped")
        return

    logger.debug("installing hook")
    client.config.hooks.append(requests_hook)
