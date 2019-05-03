"""
Core samples
"""
import logging

from samples import resource
from utils import emit


logger = logging.getLogger(__name__)


@resource('projects')
def get_projects(context):
    core_client = context.connection.clients.get_core_client()

    projects = core_client.get_projects()

    for project in projects:
        emit(project.id + ": " + project.name)

    return projects
