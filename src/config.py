import json
import os
import pathlib
import sys

from utils import emit


DEFAULT_CONFIG_FILE_NAME = "azure-devops-runner-config.json"
OLD_DEFAULT_CONFIG_FILE_NAME = "vsts-runner-config.json"
CONFIG_KEYS = [
    'url',
    'pat',
]


class Config():
    def __init__(self, filename=None):
        if not filename:
            runner_path = (pathlib.Path(os.getcwd()) / pathlib.Path(sys.argv[0])).resolve()
            filename = runner_path.parents[0] / pathlib.Path(DEFAULT_CONFIG_FILE_NAME)

        self._filename = filename

        try:
            with open(filename) as config_fp:
                self._config = json.load(config_fp)
        except FileNotFoundError:
            emit("warning: no config file found.")
            emit("The default filename has changed. You may need to rename")
            emit(OLD_DEFAULT_CONFIG_FILE_NAME)
            emit("to")
            emit(DEFAULT_CONFIG_FILE_NAME)
            self._config = {}
        except json.JSONDecodeError:
            emit("possible bug: config file exists but isn't parseable")
            self._config = {}

    def __getitem__(self, name):
        self._check_if_name_valid(name)
        return self._config.get(name, None)

    def __setitem__(self, name, value):
        self._check_if_name_valid(name)
        self._config[name] = value

    def __delitem__(self, name):
        self._check_if_name_valid(name)
        self._config.pop(name, None)

    def __len__(self):
        return len(CONFIG_KEYS)

    def __iter__(self):
        for key in CONFIG_KEYS:
            yield key

    def save(self):
        with open(self._filename, 'w') as config_fp:
            json.dump(self._config, config_fp, sort_keys=True, indent=4)

    def _check_if_name_valid(self, name):
        if name not in CONFIG_KEYS:
            raise KeyError("{0} is not a valid config key".format(name))
