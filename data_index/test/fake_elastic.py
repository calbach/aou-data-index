from data_index import elastic
import httpretty
import json
import re


class FakeElastic:
    """Fake in-memory Elastic server with limited functionality."""

    def __init__(self):
      # Index name (str) -> type (str) -> id (str) -> document (dict)
      self.indices = {}

    def put_index(self, name):
        if name in self.indices:
            return (400, {}, json.dumps({
                'error': {
                    'type': elastic.INDEX_ALREADY_EXISTS
                }
            }))
        self.indices[name] = {}
        return (200, {}, '')

    def delete_index(self, name):
        if name not in self.indices:
            return (404, {}, '')
        del self.indices[name]
        return (200, {}, '')

    def search_documents(self, index_name, doc_type):
        docs_index = self.indices.get(index_name, {}).get(doc_type)
        if docs_index is None:
            return (404, {}, '')

        # Structure matches https://www.elastic.co/guide/en/elasticsearch/reference/current/search-uri-request.html
        return (200, {}, json.dumps({
            'hits': {
                'hits': sorted(docs_index.values())
            }
        }))

    def put_document(self, index_name, doc_type, doc_id, doc, query_params):
        if index_name not in self.indices:
            # Simulate Elastic's lazy index creation.
            self.put_index(index_name)
        index = self.indices[index_name]
        if doc_type not in index:
            index[doc_type] = {}
        doc = doc.copy()
        doc['_id'] = doc_id
        if doc_id in index[doc_type] and (
            'op_type' in query_params and query_params['op_type'] == ['create']):
            return (409, {}, json.dumps({}))

        index[doc_type][doc_id] = doc
        return (200, {}, json.dumps({}))

    def get_document(self, index_name, doc_type, doc_id):
        doc = self.indices.get(index_name, {}).get(doc_type, {}).get(doc_id)
        if not doc:
            return (404, {}, '')
        return (200, {}, json.dumps(doc))

    def delete_document(self, index_name, doc_type, doc_id):
        doc = self.indices.get(index_name, {}).get(doc_type, {}).get(doc_id)
        if not doc:
            return (404, {}, '')
        del self.indices[index_name][doc_type][doc_id]
        return (200, {}, json.dumps(doc))

def index_re_fmt(base_url):
    return re.compile(base_url + '/[^/?]+(\?.*)?$')

def search_re_fmt(base_url):
    return re.compile(base_url + '/([^/]+)/([^/]+)/_search(\?.*)?$')

def doc_re_fmt(base_url):
    return re.compile(base_url + '/([^/]+)/([^/]+)/([^/?]+)(\?.*)?$')

def register_httpretty(base_url, fake):
    """Mock HTTP requests to the given URL to the given fake Elastic.

    Mocks all requests via HTTPretty at negative priority. Mocking in unit tests
    can therefore use the default priority of 0 to take precedence. In general,
    one should call httpretty.reset() in unit tests to allow custom overrides
    as binding multiple callbacks on the same endpoint may trigger httpretty's
    rotating responses.

    Args:
      base_url: (string) URL which should be routed to the fake
      fake: (FakeElastic) the fake backend instance
    """
    # Wrap index methods.
    index_re = index_re_fmt(base_url)
    def wrap_put_index(request, uri, headers):
        return fake.put_index(uri[len(base_url + '/'):])
    httpretty.register_uri(httpretty.PUT, index_re, wrap_put_index, priority=-2)

    def wrap_delete_index(request, uri, headers):
        return fake.delete_index(uri[len(base_url + '/'):])
    httpretty.register_uri(httpretty.DELETE, index_re, wrap_delete_index,
                           priority=-2)

    # Wrap document methods.
    search_re = search_re_fmt(base_url)
    def wrap_search_documents(request, uri, headers):
        m = search_re.match(uri)
        json_req = json.loads(request.body)
        return fake.search_documents(m.group(1), m.group(2))
    # doc_re also matches the search URI; take precedence with priority of -1
    httpretty.register_uri(httpretty.POST, search_re, wrap_search_documents,
                           priority=-1)

    doc_re = doc_re_fmt(base_url)
    def wrap_put_document(request, uri, headers):
        doc = json.loads(request.body)
        m = doc_re.match(uri)
        return fake.put_document(m.group(1), m.group(2), m.group(3), doc,
                                 request.querystring)
    httpretty.register_uri(httpretty.PUT, doc_re, wrap_put_document,
                           priority=-2)

    def wrap_get_document(request, uri, headers):
        m = doc_re.match(uri)
        return fake.get_document(m.group(1), m.group(2), m.group(3))
    httpretty.register_uri(httpretty.GET, doc_re, wrap_get_document,
                           priority=-2)

    def wrap_delete_document(request, uri, headers):
        m = doc_re.match(uri)
        return fake.delete_document(m.group(1), m.group(2), m.group(3))
    httpretty.register_uri(httpretty.DELETE, doc_re, wrap_delete_document,
                           priority=-2)
