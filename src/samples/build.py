"""
Build samples.
"""
import logging

from samples import resource
from utils import emit, find_any_project, find_any_build_definition


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


@resource('build')
def queue_build(context):
    definition = find_any_build_definition(context)

    build_client = context.connection.clients.get_build_client()

    build = {
        'definition': {
            'id': definition.id
        }
    }

    response = build_client.queue_build(build=build, project=definition.project.id)

    emit(str(response.id) + ": " + response.url)

    return response
