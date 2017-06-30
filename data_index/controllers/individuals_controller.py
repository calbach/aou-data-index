import connexion
from data_index.models.individual import Individual
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from werkzeug.exceptions import NotImplemented
from ..util import deserialize_date, deserialize_datetime


def create_individual(datasetId, body):
    """
    Create an individual.

    Args:
      datasetId: the parent dataset
      body: the JSON request body
    Returns:
      a dictionary representing a Individual
    """
    if connexion.request.is_json:
        body = Individual.from_dict(connexion.request.get_json())
    raise NotImplemented()


def get_individual(datasetId, individualId):
    """
    Gets an individual.

    Args:
      datasetId: the parent dataset
      individualId: the data pointer to retrieve

    Returns:
      a dictionary representation of a Individual
    """
    raise NotImplemented()


def update_individual(datasetId, individualId, body):
    """
    Updates a data pointer.

    Args:
      datasetId: the parent dataset
      individualId: the individual to update
      body: JSON representation of the updated Individual

    Returns:
      a JSON representation of the updated Individual
    """
    if connexion.request.is_json:
        body = Individual.from_dict(connexion.request.get_json())
    raise NotImplemented()


def delete_individual(datasetId, individualId):
    """
    Deletes an individual.

    Args:
      datasetId: the parent dataset
      individualId: the individual to delete
    """
    raise NotImplemented()
