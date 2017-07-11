import connexion
from data_index.models.dataset import Dataset
from data_index.models.list_datasets_response import ListDatasetsResponse
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from werkzeug.exceptions import NotImplemented
from ..util import deserialize_date, deserialize_datetime


def list_datasets(pageSize=64, pageToken=None):
    """
    Paginated method for listing all datasets in the repository.

    Args:
      pageSize: The int maximum number of datasets to return per page. The
        server may return fewer. If unspecified, defaults to 64. Maximum value
        is 1024.
      pageToken: The string continuation token, which is used to page through
        large result sets. To get the next page of results, set this parameter
        to the value of nextPageToken from the previous response.

    Returns:
      a dictionary representation of a ListDatasetsResponse
    """
    raise NotImplemented()


def create_dataset(body):
    """
    Create a dataset.

    Args:
      body: the dataset JSON

    Returns:
      a dictionary representing a Dataset
    """
    if connexion.request.is_json:
        body = Dataset.from_dict(connexion.request.get_json())
    raise NotImplemented()


def get_dataset(datasetId):
    """
    Gets a dataset.

    Args:
      datasetId: the dataset to retrieve

    Returns:
      a dictionary representation of a Dataset
    """
    raise NotImplemented()


def update_dataset(datasetId, body):
    """
    Updates a dataset.

    Args:
      datasetId: the dataset to update
      body: JSON representation of the updated Dataset

    Returns:
      a JSON representation of the updated Dataset
    """
    if connexion.request.is_json:
        body = Dataset.from_dict(connexion.request.get_json())
    raise NotImplemented()


def delete_dataset(datasetId):
    """
    Deletes a dataset.

    Args:
      datasetId: the dataset to delete
    """
    raise NotImplemented()
