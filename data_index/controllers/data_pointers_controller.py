import connexion
import requests
import urllib
from data_index import elastic
from data_index.controllers import datasets_controller, individuals_controller, names, errors
from data_index.models.data_pointer import DataPointer
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from werkzeug.exceptions import BadRequest, InternalServerError, NotImplemented
from ..util import deserialize_date, deserialize_datetime


def data_pointer_name(ds_id, uri):
  dp_id = urllib.quote(uri, safe='')
  return ('datasets/{}/dataPointers/{}'.format(ds_id, id), dp_id)


def doc_to_data_pointer(doc):
  ds_id = doc['_index'].split(':')[1]
  dp_id = urllib.quote(doc['_id'], safe='')
  return DataPointer(
      name='datasets/{}/dataPointers/{}'.format(ds_id, dp_id),
      labels=doc['_source'].copy())


def data_pointer_to_doc(dp):
  if not dp.labels:
    return {}
  return dp.labels.copy()


def create_data_pointer(datasetId, body):
    """
    Create a data pointer.

    Args:
      datasetId: the parent dataset
      body: the JSON request body

    Returns:
      a dictionary representing a DataPointer
    """
    if not connexion.request.is_json:
        raise InternalServerError('got unexpected non-JSON payload')
    dp = DataPointer.from_dict(body)
    if not dp or not dp.uri:
        raise BadRequest('missing required dataPointer.uri from request')

    # Will raise NotFound if the dataset doesn't exist.
    datasets_controller.get_dataset(datasetId)

    dp.name, dp_id = data_pointer_name(datasetId, dp.uri)
    individuals = dict()
    for name in (dp.individual_names or []):
        ind_ds_id, ind_id = names.split_individual_name(name)
        if datasetId != ind_ds_id:
            raise BadRequest('dataPointer.individualNames must belong to the same dataset as the dataPointer ("datasets/{}"), got "{}"'.format(datasetId, name))
        # Will raise NotFound if individual doesn't exist.
        # TODO(calbach): Could batch these requests.
        individuals[ind_id] = individuals_controller.get_individual(datasetId, ind_id)

    # Add the data pointer documents to the data indices.
    dp_paths = [elastic.data_by_data_index_path(datasetId, dp_id)]
    for ind_id in individuals:
        dp_paths.append(elastic.data_by_ppl_index_path(datasetId, dp_id, ind_id))

    dp_doc = data_pointer_to_doc(dp)
    for path in dp_paths:
        requests.put(path, json=dp_doc, headers=elastic.REQ_HEADERS).raise_for_status()

    # Add the associated individuals documents to the individuals (by data) index.
    for (ind_id, ind) in individuals.iteritems():
        requests.put(elastic.ppl_by_data_index_path(datasetId, ind_id, dp_id),
                     json=individuals_controller.individual_to_doc(ind),
                     headers=elastic.REQ_HEADERS).raise_for_status()

    return dp


def get_data_pointer(datasetId, dataPointerId):
    """
    Gets a data pointer.

    Args:
      datasetId: the parent dataset
      dataPointerId: the data pointer to retrieve

    Returns:
      a dictionary representation of a DataPointer
    """
    # uri = urllib.unquote(dataPointerId)
    r = requests.get(elastic.data_by_data_index_path(datasetId, dataPointerId))
    if r.status_code == requests.codes.not_found:
        raise errors.DataPointerNotFound(datasetId, dataPointerId)
    r.raise_for_status()
    return doc_to_data_pointer(r.json())


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
