"""
Utility methods likely to be useful for anyone building samples.
"""
import logging

from exceptions import AccountStateError
import http_logging


logger = logging.getLogger(__name__)


def emit(msg, *args):
    print(msg % args)


def find_any_project(context):
    logger.debug('finding any project')

    # if we already contains a looked-up project, return it
    if hasattr(context.runner_cache, 'project'):
        logger.debug('using cached project %s', context.runner_cache.project.name)
        return context.runner_cache.project

    with http_logging.temporarily_disabled():
        core_client = context.connection.clients.get_core_client()
        projects = core_client.get_projects()

    try:
        context.runner_cache.project = projects[0]
        logger.debug('found %s', context.runner_cache.project.name)
        return context.runner_cache.project
    except IndexError:
        raise AccountStateError('Your account doesn''t appear to have any projects available.')


def find_any_repo(context):
    logger.debug('finding any repo')

    # if a repo is cached, use it
    if hasattr(context.runner_cache, 'repo'):
        logger.debug('using cached repo %s', context.runner_cache.repo.name)
        return context.runner_cache.repo

    with http_logging.temporarily_disabled():
        project = find_any_project(context)
        git_client = context.connection.clients.get_git_client()
        repos = git_client.get_repositories(project.id)

    try:
        context.runner_cache.repo = repos[0]
        return context.runner_cache.repo
    except IndexError:
        raise AccountStateError('Project "%s" doesn''t appear to have any repos.' % (project.name,))
