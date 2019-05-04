"""
Build samples.
"""
import logging

from samples import resource
from utils import emit, find_any_project


logger = logging.getLogger(__name__)


@resource('definition')
def get_definitions(context):
    project = find_any_project(context)
    emit(project.name)
    build_client = context.connection.clients.get_build_client()

    definitions = build_client.get_definitions(project.id)

    for definition in definitions:
        emit(str(definition.id) + ": " + definition.name)

    return definitions
