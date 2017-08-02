import connexion
import requests
from data_index.controllers import datasets_controller, names, errors
from data_index.models.individual import Individual
from data_index import elastic
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from werkzeug.exceptions import BadRequest, InternalServerError, NotImplemented
from ..util import deserialize_date, deserialize_datetime


def doc_to_individual(doc):
  ds_id = doc['_index'].split(':')[1]
  return Individual(
      name='datasets/{}/individuals/{}'.format(ds_id, doc['_id']),
      labels=doc['_source'].copy())


def individual_to_doc(individual):
  if not individual.labels:
      return {}
  return individual.labels.copy()


def create_individual(datasetId, body):
    """
    Create an individual.

    Args:
      datasetId: the parent dataset
      body: the JSON request body
    Returns:
      a dictionary representing a Individual
    """
    if not connexion.request.is_json:
        raise InternalServerError('got unexpected non-JSON payload')
    individual = Individual.from_dict(body)
    if not individual or not individual.name:
        raise BadRequest('missing required individual.name from request')

    (ds_id, ind_id) = names.split_individual_name(individual.name)
    if ds_id != datasetId:
        raise BadRequest('dataset name "datasets/{}" from URL must agree with ' +
                         'individual.name "{}"'.format(datasetId, individual.name))

    # Will raise NotFound if the dataset doesn't exist.
    datasets_controller.get_dataset(datasetId)

    requests.put(
        elastic.ppl_by_ppl_index_path(ds_id, ind_id),
        json=individual_to_doc(individual),
        headers=elastic.REQ_HEADERS).raise_for_status()
    return individual


def get_individual(datasetId, individualId):
    """
    Gets an individual.

    Args:
      datasetId: the parent dataset
      individualId: the data pointer to retrieve

    Returns:
      a dictionary representation of a Individual
    """
    r = requests.get(elastic.ppl_by_ppl_index_path(datasetId, individualId))
    if r.status_code == requests.codes.not_found:
        raise errors.IndividualNotFound(datasetId, individualId)
    r.raise_for_status()
    return doc_to_individual(r.json())



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
