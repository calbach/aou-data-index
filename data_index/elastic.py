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
