"""
TEST samples
"""
import datetime
import logging

from samples import resource
from utils import emit


logger = logging.getLogger(__name__)


def get_project_names(context):
    core_client = context.connection.get_client("vsts.core.v4_1.core_client.CoreClient")
    return (project.name for project in core_client.get_projects())


@resource("test_plans")
def get_plans(context):
    test_client = context.connection.get_client("vsts.test.v4_1.test_client.TestClient")
    for project in get_project_names(context):
        try:
            for plan in test_client.get_plans(project):
                emit("Test Plan {}: {} ({})".format(plan.id, plan.name, plan.area.name))
        except Exception as e:
            emit("Project '{}' raised error: {}".format(project, e))


@resource("test_suites")
def get_test_suites_for_plan(context):
    test_client = context.connection.get_client("vsts.test.v4_1.test_client.TestClient")
    for project in get_project_names(context):
        try:
            for plan in test_client.get_plans(project):
                for suite in test_client.get_test_suites_for_plan(project, plan.id):
                    emit(
                        "Test Suite {}: {} ({}.{})".format(
                            suite.id, suite.name, plan.id, plan.name
                        )
                    )
        except Exception as e:
            emit("Project '{}' raised error: {}".format(project, e))


@resource("test_runs")
def get_test_runs(context):
    test_client = context.connection.get_client("vsts.test.v4_1.test_client.TestClient")
    for project in get_project_names(context):
        try:
            for run in test_client.get_test_runs(project, top=16):
                emit(
                    "Test Run {}: {} => {} ({})".format(
                        run.id, run.name, run.state, project
                    )
                )
        except Exception as e:
            emit("Project '{}' raised error: {}".format(project, e))


@resource("test_results")
def get_test_results(context):
    test_client = context.connection.get_client("vsts.test.v4_1.test_client.TestClient")
    for project in get_project_names(context):
        try:
            for run in test_client.get_test_runs(project, top=10):
                # Limiting Test Results is not something one shall do!
                for res in test_client.get_test_results(project, run.id, top=3):
                    tc = res.test_case
                    tester = res.run_by.display_name
                    emit(
                        "Test Result {}: {} => {} by {} ({})".format(
                            run.id, tc.name, res.outcome, tester, project
                        )
                    )
        except Exception as e:
            emit("Project '{}' raised error: {}".format(project, e))
