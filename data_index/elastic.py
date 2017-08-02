from flask import current_app


REQ_HEADERS = {'content-type': 'application/json'}

INDEX_ALREADY_EXISTS = 'index_already_exists_exception'


def error_type(json_resp):
  return json_resp.get('error', {}).get('type', '')


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
