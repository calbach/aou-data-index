import connexion
from swagger_server.models.cdr_data_pointer import CdrDataPointer
from swagger_server.models.cdr_dataset import CdrDataset
from swagger_server.models.cdr_individual import CdrIndividual
from swagger_server.models.cdr_list_datasets_response import CdrListDatasetsResponse
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime


def create_data_pointer(dataset_id, body):
    """
    Create a data pointer.

    Args:
      dataset_id: the parent dataset
      body: the JSON request body

    Returns:
      a dictionary representing a CdrDataPointer
    """
    if not connexion.request.is_json:
      return {}, 400
    dp = CdrDataPointer.from_dict(connexion.request.get_json())
    # TODO(calbach): Call ES.
    return dp.to_dict()


def create_dataset(body):
    """
    Create a dataset.

    Args:
      body: the dataset JSON

    Returns:
      a dictionary representing a CdrDataset
    """
    if not connexion.request.is_json:
      return {}, 400
    dataset = CdrDataset.from_dict(connexion.request.get_json())
    # TODO(calbach): Call ES.
    return dataset.to_dict()


def create_individual(dataset_id, body):
    """
    Create an individual.

    Args:
      dataset_id: the parent dataset
      body: the JSON request body

    Returns:
      a dictionary representing a CdrIndividual
    """
    if not connexion.request.is_json:
      return {}, 400
    individual = CdrIndividual.from_dict(connexion.request.get_json())
    # TODO(calbach): Call ES.
    return individual.to_dict()


def delete_data_pointer(dataset_id, data_pointer_id):
    """
    Deletes a data pointer.

    Args:
      dataset_id: the parent dataset
      data_pointer_id: the data pointer to delete
    """
    # TODO(calbach): Call ES.
    pass


def delete_dataset(dataset_id):
    """
    Deletes a dataset.

    Args:
      dataset_id: the dataset to delete
    """
    # TODO(calbach): Call ES.
    pass


def delete_individual(dataset_id, individual_id):
    """
    Deletes an individual.

    Args:
      dataset_id: the parent dataset
      individual_id: the individual to delete
    """
    # TODO(calbach): Call ES.
    pass


def get_data_pointer(dataset_id, data_pointer_id):
    """
    Gets a data pointer.

    Args:
      dataset_id: the parent dataset
      data_pointer_id: the data pointer to retrieve

    Returns:
      a dictionary representation of a CdrDataPointer
    """
    # TODO(calbach): Call ES.
    return {}


def get_dataset(dataset_id):
    """
    Gets a dataset.

    Args:
      dataset_id: the dataset to retrieve

    Returns:
      a dictionary representation of a CdrDataset
    """
    # TODO(calbach): Call ES.
    return {}


def get_individual(dataset_id, individual_id):
    """
    Gets an individual.

    Args:
      dataset_id: the parent dataset
      individual_id: the data pointer to retrieve

    Returns:
      a dictionary representation of a CdrIndividual
    """
    # TODO(calbach): Call ES.
    return {}


def list_datasets(page_size=None, page_token=None):
    """
    Lists datasets.

    Args:
      page_size: the maximum number of elements to return per-page
      page_token: pagination token for continued pagination

    Returns:
      a dictionary representation of a CdrListDatasetsResponse
    """
    # TODO(calbach): Call ES.
    return {}


def update_data_pointer(dataset_id, data_pointer_id, body):
    """
    Updates a data pointer.

    Args:
      dataset_id: the parent dataset
      data_pointer_id: the data pointer to update
      body: JSON representation of the updated CdrDataPointer

    Returns:
      a JSON representation of the updated CdrDataPointer
    """
    if not connexion.request.is_json:
      return {}, 400
    dp = CdrDataPointer.from_dict(connexion.request.get_json())
    # TODO(calbach): Call ES.
    return dp.to_dict()


def update_dataset(dataset_id, body):
    """
    Updates a dataset.

    Args:
      dataset_id: the dataset to update
      body: JSON representation of the updated CdrDataset

    Returns:
      a JSON representation of the updated CdrDataset
    """
    if not connexion.request.is_json:
      return {}, 400
    dataset = CdrDataset.from_dict(connexion.request.get_json())
    # TODO(calbach): Call ES.
    return dataset.to_dict()


def update_individual(dataset_id, individual_id, body):
    """
    Updates a data pointer.

    Args:
      dataset_id: the parent dataset
      individual_id: the individual to update
      body: JSON representation of the updated CdrIndividual

    Returns:
      a JSON representation of the updated CdrIndividual
    """
    if not connexion.request.is_json:
      return {}, 400
    individual = CdrIndividual.from_dict(connexion.request.get_json())
    # TODO(calbach): Call ES.
    return individual.to_dict()
