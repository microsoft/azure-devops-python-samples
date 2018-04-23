"""
Git samples.
"""
import logging

from samples import resource
from utils import emit, find_any_project, find_any_repo


logger = logging.getLogger(__name__)


@resource('repositories')
def get_repos(context):
    project = find_any_project(context)

    git_client = context.connection.get_client("vsts.git.v4_1.git_client.GitClient")

    repos = git_client.get_repositories(project.id)

    for repo in repos:
        emit(repo.id + ": " + repo.name)

    return repos


@resource('refs')
def get_refs(context):
    repo = find_any_repo(context)

    git_client = context.connection.get_client("vsts.git.v4_1.git_client.GitClient")

    refs = git_client.get_refs(repo.id, repo.project.id)

    for ref in refs:
        emit(ref.name + ": " + ref.object_id)

    return refs
