import connexion
from data_index.models.data_pointer import DataPointer
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from werkzeug.exceptions import NotImplemented
from ..util import deserialize_date, deserialize_datetime


def create_data_pointer(datasetId, body):
    """
    Create a data pointer.

    Args:
      datasetId: the parent dataset
      body: the JSON request body

    Returns:
      a dictionary representing a DataPointer
    """
    if connexion.request.is_json:
        body = DataPointer.from_dict(connexion.request.get_json())
    raise NotImplemented()


def get_data_pointer(datasetId, dataPointerId):
    """
    Gets a data pointer.

    Args:
      datasetId: the parent dataset
      dataPointerId: the data pointer to retrieve

    Returns:
      a dictionary representation of a DataPointer
    """
    raise NotImplemented()


def update_data_pointer(datasetId, dataPointerId, body):
    """
    Updates a data pointer.

    Args:
      datasetId: the parent dataset
      dataPointerId: the data pointer to update
      body: JSON representation of the updated DataPointer

    Returns:
      a JSON representation of the updated DataPointer
    """
    if connexion.request.is_json:
        body = DataPointer.from_dict(connexion.request.get_json())
    raise NotImplemented()


def delete_data_pointer(datasetId, dataPointerId):
    """
    Deletes a data pointer.

    Args:
      datasetId: the parent dataset
      dataPointerId: the data pointer to delete
    """
    raise NotImplemented()
