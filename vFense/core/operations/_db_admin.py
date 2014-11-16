import logging, logging.config

from vFense._constants import VFENSE_LOGGING_CONFIG
from vFense.core.decorators import time_it, catch_it
from vFense.db.client import db_create_close, r
from vFense.core._db import (
    insert_data_in_table, update_data_in_table
)

from vFense.core.operations._db_model import (
    OperationCollections
)

logging.config.fileConfig(VFENSE_LOGGING_CONFIG)
logger = logging.getLogger('vfense_api')

@time_it
@catch_it({})
@db_create_close
def fetch_admin_operation(operation_id, conn=None):
    """Fetch an operation by id and all of it's information
    Args:
        operation_id (str): 36 character UUID

    Basic Usage:
        >>> from vFense.core.operations._db_admin import fetch_admin_operation
        >>> operation_id = '8fed3dc7-33d4-4278-9bd4-398a68bf7f22'
        >>> fetch_admin_operation(operation_id)

    Returns:
        Dictionary
    """
    data = (
        r
        .table(OperationCollections.Admin)
        .get(operation_id)
        .run(conn)
    )

    return data

def insert_admin_operation(data):
    results = (
        insert_data_in_table(data, OperationCollections.Admin)
    )

    return results


def update_admin_operation(operation_id, data):
    results = (
        update_data_in_table(operation_id, data, OperationCollections.Admin)
    )

    return results
