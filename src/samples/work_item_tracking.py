"""
WIT samples
"""
import datetime
import logging

from samples import resource
from utils import emit


logger = logging.getLogger(__name__)


@resource('work_items')
def get_work_items(context):
    wit_client = context.connection.get_client(
        "vsts.work_item_tracking.v4_1.work_item_tracking_client.WorkItemTrackingClient")

    desired_ids = range(1, 51)
    work_items = wit_client.get_work_items(ids=desired_ids, error_policy="omit")

    for id_, work_item in zip(desired_ids, work_items):
        if work_item:
            emit("{0} {1}: {2}".format(work_item.fields['System.WorkItemType'],
                                       work_item.id,
                                       work_item.fields['System.Title']))
        else:
            emit("(work item {0} omitted by server)".format(id_))

    return work_items


@resource('work_items')
def get_work_items_as_of(context):
    wit_client = context.connection.get_client(
        "vsts.work_item_tracking.v4_1.work_item_tracking_client.WorkItemTrackingClient")

    desired_ids = range(1, 51)
    as_of_date = datetime.datetime.now() + datetime.timedelta(days=-7)
    work_items = wit_client.get_work_items(ids=desired_ids, as_of=as_of_date, error_policy="omit")

    for id_, work_item in zip(desired_ids, work_items):
        if work_item:
            emit("{0} {1}: {2}".format(work_item.fields['System.WorkItemType'],
                                       work_item.id,
                                       work_item.fields['System.Title']))
        else:
            emit("(work item {0} omitted by server)".format(id_))

    return work_items
