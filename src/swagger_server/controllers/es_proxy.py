from flask import Blueprint, current_app, request
import requests

proxy = Blueprint('es_proxy', __name__)

def index_addr():
  return current_app.config['INDEX_ADDR']


@proxy.route('/es/<path:es_path>')
def do_proxy(es_path):
  """A hacky proxy to ElasticSearch.

  This proxy will later be replaced with a selective whitelisting of
  ElasticSearch functionality, defined in the Swagger API layer.

  Args:
    es_path: str path for the requested elastic search path

  Returns:
    an HTTP response in bytes
  """
  r = requests.request(
      request.method,
      index_addr() + '/' + es_path,
      params=request.query_string,
      data=request.get_json())
  r.raise_for_status()
  return r.content
