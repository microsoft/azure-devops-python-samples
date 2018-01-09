"""
Core samples
"""
import logging

from samples import resource
from utils import emit


logger = logging.getLogger(__name__)


@resource('projects')
def get_projects(context):
    core_client = context.connection.get_client("vsts.core.v4_1.core_client.CoreClient")

    projects = core_client.get_projects()

    for project in projects:
        emit(project.id + ": " + project.name)

    return projects
