"""
Azure DevOps Python API sample runner.
"""
import argparse
import logging
import os
import pathlib
import sys
from types import SimpleNamespace

# logging.basicConfig(level=logging.INFO)

from vsts.credentials import BasicAuthentication
from vsts.vss_connection import VssConnection

from config import Config
import http_logging
import hacks
import runner_lib
from utils import emit

__VERSION__ = "1.0.0"

logger = logging.getLogger(__name__)


def main(url, area, resource, auth_token, output_path=None):

    context = SimpleNamespace()
    context.runner_cache = SimpleNamespace()

    # setup the connection
    context.connection = VssConnection(
        base_url=url,
        creds=BasicAuthentication('PAT', auth_token),
        user_agent='azure-devops-python-samples/' + __VERSION__)

    # if the user asked for logging:
    # - add a hook for logging the http request
    # - create the root directory
    if output_path:
        # monkey-patch the get_client method to attach our hook
        _get_client = context.connection.get_client

        def get_client_with_hook(*args, **kwargs):
            logger.debug("get_client_with_hook")
            client = _get_client(*args, **kwargs)
            hacks.add_request_hook(client)
            return client
        context.connection.get_client = get_client_with_hook

        root_log_dir = pathlib.Path(output_path)
        if not root_log_dir.exists():
            root_log_dir.mkdir(parents=True, exist_ok=True)
        http_logging.push_state(True)
    else:
        root_log_dir = None

    # runner_lib.discovered_samples will contain a key for each area loaded,
    # and each key will have the resources and sample functions discovered
    if area == 'all':
        areas = runner_lib.discovered_samples.keys()
    else:
        if area not in runner_lib.discovered_samples.keys():
            raise ValueError("area '%s' doesn't exist" % (area,))
        areas = [area]

    for area in areas:

        area_logging_path = runner_lib.enter_area(area, root_log_dir)

        for area_resource, functions in runner_lib.discovered_samples[area].items():
            if area_resource != resource and resource != 'all':
                logger.debug("skipping resource %s", area_resource)
                continue

            resource_logging_path = runner_lib.enter_resource(area_resource, area_logging_path)

            for run_sample in functions:
                runner_lib.before_run_sample(run_sample.__name__, resource_logging_path)
                run_sample(context)
                runner_lib.after_run_sample(resource_logging_path)


def list_cmd(args, config):
    template = "  <{0}>: {1}"
    print()
    print("Available <area>s and resources")
    print(template.format("all", "all"))
    for area in runner_lib.discovered_samples.keys():
        resources = ", ".join(runner_lib.discovered_samples[area].keys())
        print(template.format(area, resources))
    print()
    print("For any area, you can always pass 'all' to run all resource samples")


def run_cmd(args, config):
    try:
        auth_token = os.environ['AZURE_DEVOPS_PAT']
    except KeyError:
        if config['pat']:
            emit("Using auth token from config file")
            auth_token = config['pat']
        else:
            emit('You must first set the AZURE_DEVOPS_PAT environment variable or the `pat` config setting')
            sys.exit(1)

    if not args.url:
        if config['url']:
            args.url = config['url']
            emit('Using configured URL {0}'.format(args.url))
        else:
            emit('No URL configured - pass it on the command line')
            sys.exit(1)

    args_dict = vars(args)

    main(**args_dict, auth_token=auth_token)


def config_cmd(args, config):
    template = "  {0}: {1}"

    if args.name == 'all':
        emit("Configured settings")
        for name in config:
            emit(template.format(name, config[name]))
        return

    args.name = args.name.lower()

    if args.set_to:
        if args.name in config:
            config[args.name] = args.set_to
            emit("Setting new value for {0}".format(args.name))
            emit(template.format(args.name, config[args.name]))
            config.save()
        else:
            emit("There's no setting called {0}".format(args.name))

    elif args.delete:
        if args.name in config:
            emit("Deleting {0}; old value was".format(args.name))
            emit(template.format(args.name, config[args.name]))
            del config[args.name]
            config.save()
        else:
            emit("There's no setting called {0}".format(args.name))

    else:
        if args.name in config:
            emit(template.format(args.name, config[args.name]))
        else:
            emit("There's no setting called {0}".format(args.name))


if __name__ == '__main__':

    # main parser
    parser = argparse.ArgumentParser(description='Azure DevOps Python API samples')
    subparsers = parser.add_subparsers()

    # "list"
    discover_parser = subparsers.add_parser('list')
    discover_parser.set_defaults(dispatch=list_cmd)

    # "run"
    run_parser = subparsers.add_parser('run')
    run_parser.add_argument('area', help='Product area to run samples for, or `all`')
    run_parser.add_argument('resource', help='Resource to run samples for, or `all`')
    run_parser.add_argument('-u', '--url', help='Base URL of your Azure DevOps or TFS instance')
    run_parser.add_argument('-o', '--output-path', help='Root folder to save request/response data',
                            metavar='DIR')
    run_parser.set_defaults(dispatch=run_cmd)

    # "config"
    config_parser = subparsers.add_parser('config')
    config_parser.add_argument('name', help='Name of setting to get or set, or `all` to list all of them')
    config_parser.add_argument('--set-to', help='New value for setting')
    config_parser.add_argument('--delete', help='New value for setting', action='store_true')
    config_parser.set_defaults(dispatch=config_cmd)

    args = parser.parse_args()
    if 'dispatch' in args:
        cmd = args.dispatch
        del args.dispatch
        cmd(args, Config())
    else:
        parser.print_usage()
