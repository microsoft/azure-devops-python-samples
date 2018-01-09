"""
Helper methods moved out of the main runner file.
"""
import importlib
import logging
import pathlib
import pkgutil

import http_logging
from utils import emit

logger = logging.getLogger(__name__)

###
# Sample discovery
###

SAMPLES_MODULE_NAME = 'samples'

logger.debug("loading samples module")
_samples_module = importlib.import_module(SAMPLES_MODULE_NAME)

logger.debug('loading all modules in `%s`', SAMPLES_MODULE_NAME)
for _, name, _ in pkgutil.iter_modules(_samples_module.__path__):
    importlib.import_module('%s.%s' % (SAMPLES_MODULE_NAME, name))

# trim the sample module name off the area names
discovered_samples = {
    area[len(SAMPLES_MODULE_NAME)+1:]: module for area, module in _samples_module.discovered_samples.items()
}


###
# Logging helpers and so on
###

def enter_area(area, http_logging_path):
    emit("== %s ==", area)

    if http_logging_path is not None:
        area_log_dir = pathlib.Path(http_logging_path / area)
        area_log_dir.mkdir(parents=True, exist_ok=True)
        return area_log_dir

    return None


def enter_resource(resource, http_logging_path):
    emit("-- %s --", resource)

    if http_logging_path is not None:
        resource_log_dir = pathlib.Path(http_logging_path / resource)
        resource_log_dir.mkdir(parents=True, exist_ok=True)
        return resource_log_dir

    return None


def before_run_sample(func_name, http_logging_path):
    if http_logging_path is not None:
        example_log_file = pathlib.Path(http_logging_path / (func_name + '.json'))
        http_logging.target = example_log_file.open('w')


def after_run_sample(http_logging_path):
    if http_logging_path is not None:
        http_logging.target.close()
        http_logging.target = None
