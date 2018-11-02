"""
WIT samples
"""
import datetime
import logging

from samples import resource
from utils import emit

from vsts.work_item_tracking.v4_1.models.wiql import Wiql

logger = logging.getLogger(__name__)


def print_work_item(work_item):
    emit(
        "{0} {1}: {2}".format(
            work_item.fields["System.WorkItemType"],
            work_item.id,
            work_item.fields["System.Title"],
        )
    )


@resource("work_items")
def get_work_items(context):
    wit_client = context.connection.get_client(
        "vsts.work_item_tracking.v4_1.work_item_tracking_client.WorkItemTrackingClient"
    )

    desired_ids = range(1, 51)
    work_items = wit_client.get_work_items(ids=desired_ids, error_policy="omit")

    for id_, work_item in zip(desired_ids, work_items):
        if work_item:
            print_work_item(work_item)
        else:
            emit("(work item {0} omitted by server)".format(id_))

    return work_items


@resource("work_items")
def get_work_items_as_of(context):
    wit_client = context.connection.get_client(
        "vsts.work_item_tracking.v4_1.work_item_tracking_client.WorkItemTrackingClient"
    )

    desired_ids = range(1, 51)
    as_of_date = datetime.datetime.now() + datetime.timedelta(days=-7)
    work_items = wit_client.get_work_items(
        ids=desired_ids, as_of=as_of_date, error_policy="omit"
    )

    for id_, work_item in zip(desired_ids, work_items):
        if work_item:
            print_work_item(work_item)
        else:
            emit("(work item {0} omitted by server)".format(id_))

    return work_items


@resource("wiql_query")
def wiql_query(context):
    wit_client = context.connection.get_client(
        "vsts.work_item_tracking.v4_1.work_item_tracking_client.WorkItemTrackingClient"
    )
    wiql = Wiql(
        query="""
        select [System.Id],
            [System.WorkItemType],
            [System.Title],
            [System.State],
            [System.AreaPath],
            [System.IterationPath],
            [System.Tags]
        from WorkItems
        where [System.WorkItemType] = 'Test Case'
        order by [System.ChangedDate] desc"""
    )
    # We limit number of results to 30 on purpose
    wiql_results = wit_client.query_by_wiql(wiql, top=30).work_items
    emit("Results: {0}".format(len(wiql_results)))
    if wiql_results:
        # WIQL query gives a WorkItemReference with ID only
        # => we get the corresponding WorkItem from id
        work_items = (
            wit_client.get_work_item(int(res.id)) for res in wiql_results
        )
        for work_item in work_items:
            print_work_item(work_item)
        return work_items
    else:
        return []
