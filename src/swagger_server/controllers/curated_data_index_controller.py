import base64
import connexion
import json
import urllib
import requests
from errors import DatasetNotFound, IndividualNotFound
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound
from swagger_server.models.cdr_data_pointer import CdrDataPointer
from swagger_server.models.cdr_dataset import CdrDataset
from swagger_server.models.cdr_individual import CdrIndividual
from swagger_server.models.cdr_list_datasets_response import CdrListDatasetsResponse
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

# TODO(calbach): Figure out how to plumb parameters through, not globals.
INDEX_ADDR = 'http://localhost:9200'
ES_HEADERS = {'content-type': 'application/json'}


def ds_index_type():
  return INDEX_ADDR + '/cdr/datasets'


def ds_index_path(ds_id):
  return ds_index_type() + '/' + ds_id


def by_ppl_index(ds_id):
  return INDEX_ADDR + '/by-individual:' + ds_id


def by_data_index(ds_id):
  return INDEX_ADDR + '/by-data:' + ds_id


def ppl_by_ppl_index_path(ds_id, id):
  return by_ppl_index(ds_id) + '/individuals/' + id


def data_by_ppl_index_path(ds_id, uri, ind_id):
  return by_ppl_index(ds_id) + '/data/{}?parent={}'.format(
      urllib.urlencode(uri), ind_id)


def data_by_data_index_path(ds_id, uri):
  return by_data_index(ds_id) + '/data/' + urllib.urlencode(uri)


def ppl_by_data_index_path(ds_id, indID, uri):
  return by_data_index(ds_id) + '/individuals/{}?parent={}'.format(
      indID, urllib.urlencode(uri))


def split_ds_name(ds_name):
  parts = ds_name.split('/')
  if len(parts) != 2 or parts[0] != 'datasets':
    raise BadRequest('malformed dataset name "{}"'.format(ds_name))
  return parts[1]


def split_individual_name(name):
  parts = name.split('/')
  if len(parts) != 4 or parts[0] != 'datasets' or parts[2] != 'individuals':
    raise BadRequest('malformed individual name "{}"'.format(name))
  return (parts[1], parts[3])


def doc_to_dataset(doc):
  return CdrDataset(name='datasets/' + doc['_id'])


def dataset_to_doc(dataset):
  return {}


def doc_to_individual(doc):
  ds_id = doc['_index'].split(':')[1]
  return CdrIndividual(
      name='datasets/{}/individuals/{}'.format(ds_id, doc['_id']),
      labels=doc['_source'].copy(),)


def individual_to_doc(individual):
  return individual.labels.copy()


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
    raise InternalServerError('got unexpected non-JSON payload')
  dp = CdrDataPointer.from_dict(body)
  if not dp or not dp.Uri:
    raise BadRequest('missing required dataPointer.uri from request')
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
    raise InternalServerError('got unexpected non-JSON payload')
  dataset = CdrDataset.from_dict(body)
  if not dataset or not dataset.name:
    raise BadRequest('missing required dataset.name from request')

  ds_id = split_ds_name(dataset.name)
  requests.put(
      ds_index_path(ds_id), json={}, headers=ES_HEADERS).raise_for_status()
  requests.put(
      by_ppl_index(ds_id),
      json={
          'mappings': {
              'individuals': {},
              'data': {
                  '_parent': {
                      'type': 'individuals',
                  },
              },
          },
      },
      headers=ES_HEADERS).raise_for_status()
  requests.put(
      by_data_index(ds_id),
      json={
          'mappings': {
              'data': {},
              'individuals': {
                  '_parent': {
                      'type': 'data',
                  },
              },
          },
      },
      headers=ES_HEADERS).raise_for_status()
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
    raise InternalServerError('got unexpected non-JSON payload')
  individual = CdrIndividual.from_dict(body)
  if not individual or not individual.name:
    raise BadRequest('missing required individual.name from request')

  (ds_id, ind_id) = split_individual_name(individual.name)
  if ds_id != dataset_id:
    raise BadRequest('dataset name "datasets/{}" from URL must agree with ' +
                     'individual.name "{}"'.format(dataset_id, individual.name))

  # Will raise NotFound if the dataset doesn't exist.
  get_dataset(dataset_id)

  requests.put(
      ppl_by_ppl_index_path(ds_id, ind_id),
      json=individual_to_doc(individual),
      headers=ES_HEADERS).raise_for_status()
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
  all_not_found = True
  for path in [
      ds_index_path(dataset_id),
      by_ppl_index(dataset_id),
      by_data_index(dataset_id)
  ]:
    r = requests.delete(path)
    if r.status_code != requests.codes.not_found:
      all_not_found = False
      r.raise_for_status()

  if all_not_found:
    raise DatasetNotFound(dataset_id)

def delete_individual(dataset_id, individual_id):
  """
    Deletes an individual.

    Args:
      dataset_id: the parent dataset
      individual_id: the individual to delete
    """
  all_not_found = True
  r = requests.delete(
      ppl_by_ppl_index_path(dataset_id, individual_id))
  if r.status_code != requests.codes.not_found:
    all_not_found = False
    r.raise_for_status()

  r = requests.post(
      by_data_index(dataset_id) + '/individuals/_delete_by_query',
      json={
          'query': {
              'term': {
                  '_id': individual_id
              },
          },
      },
      headers=ES_HEADERS).raise_for_status()
  if r.status_code != requests.codes.not_found:
    all_not_found = False
    r.raise_for_status()

  if all_not_found:
    raise IndividualNotFound(dataset_id, individual_id)


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
  r = requests.get(ds_index_path(dataset_id))
  if r.status_code == requests.codes.not_found:
    raise DatasetNotFound(dataset_id)
  r.raise_for_status()
  return doc_to_dataset(r.json())


def get_individual(dataset_id, individual_id):
  """
    Gets an individual.

    Args:
      dataset_id: the parent dataset
      individual_id: the data pointer to retrieve

    Returns:
      a dictionary representation of a CdrIndividual
    """
  r = requests.get(ppl_by_ppl_index_path(dataset_id, individual_id))
  if r.status_code == requests.codes.not_found:
    raise IndividualNotFound(dataset_id, individual_id)
  r.raise_for_status()
  return doc_to_individual(r.json())


def encode_ds_page_token(offset):
  """Encode the dataset pagination token."""
  # We implement the pagination token via base64-encoded JSON s.t. tokens are
  # opaque to clients and enable us to make backwards compatible changes to our
  # pagination implementation. Base64+JSON are used specifically as they are
  # language-independent standards.
  s = json.dumps({
      'offset': offset,
  })
  # Strip ugly base64 padding.
  return base64.urlsafe_b64encode(s).rstrip('=')


def decode_ds_page_token(token):
  """Decode the dataset pagination token."""
  padded_token = token + '=' * (len(token) % 4)
  tok = base64.urlsafe_b64decode(padded_token)
  return json.loads(tok)


def list_datasets(page_size=32, page_token=None):
  """
    Lists datasets.

    Args:
      page_size: the maximum number of elements to return per-page
      page_token: pagination token for continued pagination

    Returns:
      a dictionary representation of a CdrListDatasetsResponse
    """
  es_req = {
      'size': page_size + 1,
      'query': {
          'match_all': {},
      },
      'sort': [
          '_doc',  # Index order.
      ],
  }
  offset = 0
  if page_token:
    tok = decode_ds_page_token(page_token)
    offset = tok.get('offset')
    es_req['from'] = offset

  r = requests.post(
      ds_index_type() + '/_search', json=es_req, headers=ES_HEADERS)
  r.raise_for_status()

  next_page_token = None
  hits = r.json().get('hits').get('hits')
  if len(hits) > page_size:
    hits = hits[:-1]
    next_page_token = encode_ds_page_token(offset + page_size)
  return CdrListDatasetsResponse(
      datasets=[doc_to_dataset(d) for d in hits],
      next_page_token=next_page_token,).to_dict()


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
    raise InternalServerError('got unexpected non-JSON payload')
  dp = CdrDataPointer.from_dict(body)
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
    raise InternalServerError('got unexpected non-JSON payload')
  dataset = CdrDataset.from_dict(body)
  if dataset.name:
    ds_id = split_ds_name(dataset.name)
    if ds_id != dataset_id:
      raise BadRequest(
          'URL dataset name "datasets/{}" and dataset.name "{}" must agree',
          dataset_id, dataset.name)

  r = requests.post(
      ds_index_path(dataset_id) + '/_update',
      json={
          'doc': dataset_to_doc(dataset),
      },
      headers=ES_HEADERS)
  r.raise_for_status()
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
    raise InternalServerError('got unexpected non-JSON payload')
  individual = CdrIndividual.from_dict(body)

  if individual.name:
    (ds_id, ind_id) = split_individual_name(individual.name)
    if ds_id != dataset_id or individual_id != ind_id:
      raise BadRequest('URL name "datasets/{}/individuals/{}" and ' +
                       'individual.name "{}" must agree', dataset_id,
                       individual_id, individual.name)
  else:
    individual.name = 'datasets/{}/individuals/{}'.format(
        dataset_id, individual_id)

  delete_individual(dataset_id, individual_id)
  return create_individual(dataset_id, individual.to_dict())
