import base64
import connexion
import json
import urllib
import requests
import errors
from flask import current_app
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound
from swagger_server.models.cdr_data_pointer import CdrDataPointer
from swagger_server.models.cdr_dataset import CdrDataset
from swagger_server.models.cdr_individual import CdrIndividual
from swagger_server.models.cdr_list_datasets_response import CdrListDatasetsResponse
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

# TODO(calbach): Sanitize IDs (no ':') and any strings we're feeding into ES.
ES_HEADERS = {'content-type': 'application/json'}


def index_addr():
  return current_app.config['INDEX_ADDR']


def ds_index_type():
  return index_addr() + '/cdr/datasets'


def ds_index_path(ds_id):
  return ds_index_type() + '/' + ds_id


def by_ppl_index(ds_id):
  return index_addr() + '/by-individual:' + ds_id


def by_data_index(ds_id):
  return index_addr() + '/by-data:' + ds_id


def ppl_by_ppl_index_path(ds_id, id):
  return by_ppl_index(ds_id) + '/individuals/' + id


def data_by_ppl_index_path(ds_id, dp_id, ind_id):
  return by_ppl_index(ds_id) + '/data/{}:{}?parent={}'.format(
      ind_id, dp_id, ind_id)


def data_by_data_index_path(ds_id, dp_id):
  return by_data_index(ds_id) + '/data/' + dp_id


def ppl_by_data_index_path(ds_id, indID, dp_id):
  return by_data_index(ds_id) + '/individuals/{}:{}?parent={}'.format(
      dp_id, indID, dp_id)


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


def data_pointer_name(ds_id, uri):
  id = urllib.quote(uri, safe='')
  return ('/datasets/{}/dataPointers/{}'.format(ds_id, id), id)


def split_data_pointer_name(name):
  parts = name.split('/')
  if len(parts) != 4 or parts[0] != 'datasets' or parts[2] != 'dataPointers':
    raise BadRequest('malformed dataPointer name "{}"'.format(name))
  return (parts[1], parts[3])


def doc_to_dataset(doc):
  return CdrDataset(name='datasets/' + doc['_id'])


def dataset_to_doc(dataset):
  return {}


def doc_to_individual(doc):
  ds_id = doc['_index'].split(':')[1]
  return CdrIndividual(
      name='datasets/{}/individuals/{}'.format(ds_id, doc['_id']),
      labels=doc['_source'].copy())


def individual_to_doc(individual):
  if not individual.labels:
    return {}
  return individual.labels.copy()


def doc_to_data_pointer(doc):
  ds_id = doc['_index'].split(':')[1]
  return CdrDataPointer(
      name='datasets/{}/dataPointers/{}'.format(ds_id, doc['_id']),
      labels=doc['_source'].copy())


def data_pointer_to_doc(dp):
  if not dp.labels:
    return {}
  return dp.labels.copy()


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
  if not dp or not dp.uri:
    raise BadRequest('missing required dataPointer.uri from request')

  # Will raise NotFound if the dataset doesn't exist.
  get_dataset(dataset_id)

  dp.name, dp_id = data_pointer_name(dataset_id, dp.uri)
  individuals = dict()
  for name in (dp.individual_names or []):
    ind_ds_id, ind_id = split_individual_name(name)
    if dataset_id != ind_ds_id:
      raise BadRequest('dataPointer.individualNames must belong to the same dataset as the dataPointer ("datasets/{}"), got "{}"'.format(dataset_id, name))
    # Will raise NotFound if individual doesn't exist.
    # TODO(calbach): Could batch these requests.
    individuals[ind_id] = get_individual(dataset_id, ind_id)

  # Add the data pointer documents to the data indices.
  dp_paths = [data_by_data_index_path(dataset_id, dp_id)]
  for ind_id in individuals:
    dp_paths.append(data_by_ppl_index_path(dataset_id, dp_id, ind_id))

  dp_doc = data_pointer_to_doc(dp)
  for path in dp_paths:
    requests.put(path, json=dp_doc, headers=ES_HEADERS).raise_for_status()

  # Add the associated individuals documents to the individuals (by data) index.
  for (ind_id, ind) in individuals.iteritems():
    requests.put(ppl_by_data_index_path(dataset_id, ind_id, dp_id),
                 json=individual_to_doc(ind),
                 headers=ES_HEADERS).raise_for_status()

  return dp


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
  return dataset


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
  return individual


def delete_data_pointer(dataset_id, data_pointer_id):
  """
    Deletes a data pointer.

    Args:
      dataset_id: the parent dataset
      data_pointer_id: the data pointer to delete
    """
  # Find IDs for all child individuals.
  child_docs_json = {
      'query': {
          'parent_id': {
              'type': 'individuals',
              'id': data_pointer_id
          }
      }
  }
  r = requests.post(by_data_index(dataset_id) + '/individuals/_search',
                    json=child_docs_json, headers=ES_HEADERS)
  r.raise_for_status()

  # Prepare to delete this dataPointer wherever it appears in the data-by-ppl
  # index. This is not a simple query by ID because the doc IDs in this index
  # contain the parent individual ID as well.
  to_delete = []
  for hit in r.json().get('hits').get('hits', []):
    doc_id = hit.get('_id')
    parts = doc_id.split(':')
    if len(parts) != 2:
      raise InternalServerError('malformed index doc ID "{}"'.format(doc_id))
    ind_id = parts[1]
    to_delete.append(data_by_ppl_index_path(dataset_id, data_pointer_id, ind_id))

  all_not_found = True

  # Prepare to delete the parent data document.
  to_delete.append(data_by_data_index_path(dataset_id, data_pointer_id))
  for path in to_delete:
    r = requests.delete(path)
    if r.status_code != requests.codes.not_found:
      all_not_found = False
      r.raise_for_status()

  # Lastly, delete the data document's children. This must be the final step as
  # the client would not otherwise be able to retry a partially failed delete.
  r = requests.post(by_data_index(dataset_id) + '/individuals/_delete_by_query',
                json=child_docs_json, headers=ES_HEADERS)
  r.raise_for_status()
  if r.json().get('deleted', 0) > 0:
    all_not_found = False

  if all_not_found:
    raise errors.DataPointerNotFound(dataset_id, data_pointer_id)


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
    raise errors.DatasetNotFound(dataset_id)

def delete_individual(dataset_id, individual_id):
  """
    Deletes an individual.

    Args:
      dataset_id: the parent dataset
      individual_id: the individual to delete
    """
  # Find IDs for all child data pointers.
  child_docs_json = {
      'query': {
          'parent_id': {
              'type': 'data',
              'id': individual_id
          }
      }
  }
  r = requests.post(by_ppl_index(dataset_id) + '/data/_search',
                    json=child_docs_json, headers=ES_HEADERS)
  r.raise_for_status()

  # Prepare to delete this individual wherever it appears in the ppl-by-data
  # index. This is not a simple query by ID because the doc IDs in this index
  # contain the parent data pointer ID as well.
  to_delete = []
  for hit in r.json().get('hits').get('hits', []):
    doc_id = hit.get('_id')
    parts = doc_id.split(':')
    if len(parts) != 2:
      raise InternalServerError('malformed index doc ID "{}"'.format(doc_id))
    dp_id = parts[1]
    to_delete.append(ppl_by_data_index_path(dataset_id, individual_id, dp_id))

  all_not_found = True

  # Prepare to delete the parent individual.
  to_delete.append(ppl_by_ppl_index_path(dataset_id, individual_id))
  for path in to_delete:
    r = requests.delete(path)
    if r.status_code != requests.codes.not_found:
      all_not_found = False
      r.raise_for_status()

  # Lastly, delete the individual document's children. This must be the final
  # step as the client would not otherwise be able to retry a partially failed
  # delete.
  r = requests.post(by_ppl_index(dataset_id) + '/data/_delete_by_query',
                json=child_docs_json, headers=ES_HEADERS)
  r.raise_for_status()
  if r.json().get('deleted', 0) > 0:
    all_not_found = False

  if all_not_found:
    raise errors.IndividualNotFound(dataset_id, individual_id)


def get_data_pointer(dataset_id, data_pointer_id):
  """
    Gets a data pointer.

    Args:
      dataset_id: the parent dataset
      data_pointer_id: the data pointer to retrieve

    Returns:
      a dictionary representation of a CdrDataPointer
    """
  uri = urllib.unquote(data_pointer_id)
  r = requests.get(data_by_data_index_path(dataset_id, uri))
  if r.status_code == requests.codes.not_found:
    raise errors.DataPointerNotFound(dataset_id, data_pointer_id)
  r.raise_for_status()
  return doc_to_data_pointer(r.json())


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
    raise errors.DatasetNotFound(dataset_id)
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
    raise errors.IndividualNotFound(dataset_id, individual_id)
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
      next_page_token=next_page_token,)


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

  if dp.name:
    (ds_id, dp_id) = split_individual_name(dp.name)
    if ds_id != dataset_id or data_pointer_id != dp_id:
      raise BadRequest('URL name "datasets/{}/dataPointers/{}" and ' +
                       'dataPointer.name "{}" must agree', dataset_id,
                       data_pointer_id, dp.name)
  else:
    dp.name = 'datasets/{}/dataPointers/{}'.format(
        dataset_id, data_pointer_id)

  delete_data_pointer(dataset_id, data_pointer_id)
  return create_data_pointer(dataset_id, dp.to_dict())


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
  else:
    dataset.name = 'datasets/' + dataset_id

  delete_dataset(dataset_id)
  return create_dataset(dataset.to_dict())


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
