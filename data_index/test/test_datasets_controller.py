from __future__ import absolute_import

import base64
import doctest
import httpretty
import unittest
from data_index.controllers import datasets_controller
from data_index.models.dataset import Dataset
from data_index.models.list_datasets_response import ListDatasetsResponse
from data_index.test import BaseTestCase, fake_elastic
from six import BytesIO
from flask import json
from parameterized import param, parameterized


class TestDatasetsController(BaseTestCase):
    """Datasets tests."""

    @parameterized.expand([
        ('page size 1', 1, 3),
        ('page size 2', 2, 2),
        ('page size 3', 3, 1),
        ('page size 4', 4, 1),
        ('page size large', 99999, 1),
        ('default', None, 1),
    ])
    def test_list_datasets(self, _, page_size, expected_pages):
        datasets = [
            Dataset(name='datasets/a'),
            Dataset(name='datasets/b'),
            Dataset(name='datasets/c'),
        ]
        dataset_docs = []
        for d in datasets:
            ds_id = d.name[len('datasets/'):]
            dataset_docs.append({
                '_id': ds_id,
                'source': {'id': ds_id},
            })
        expected = [d.to_dict() for d in datasets]

        search_re = fake_elastic.search_re_fmt(BaseTestCase.INDEX_ADDR)
        def wrap_search_documents(request, uri, _):
            m = search_re.match(uri)
            json_req = json.loads(request.body)
            start = 0
            gte_id = json_req.get('query', {}).get('range', {}).get('id', {}).get('gte')
            if gte_id:
                gte_name = 'datasets/' + gte_id
                for i, d in enumerate(datasets):
                    if d.name >= gte_name:
                        start = i
                        break
            to = len(datasets)
            size = json_req.get('size')
            if size:
                to = min(start + size, len(datasets))
            return (200, {}, json.dumps({
                'hits': {
                    'hits': dataset_docs[start:to]
                }
            }))
        # Ignore the default test setup.
        httpretty.reset()
        httpretty.register_uri(httpretty.POST, search_re, wrap_search_documents)

        got = []
        got_pages = 0
        page_token = None
        for _ in range(100):
            query_string = []
            if page_size is not None:
                query_string.append(('pageSize', page_size))
            if page_token is not None:
                query_string.append(('pageToken', page_token))
            response = self.client.open(
                '/v1/datasets',
                method='GET',
                content_type='application/json',
                query_string=query_string)
            self.assertStatus(response, 200)
            got_pages += 1
            datasets_json = response.json.get('datasets', [])
            if page_size is not None:
                self.assertLessEqual(len(datasets_json), page_size)
            got.extend(datasets_json)
            page_token = response.json.get('nextPageToken')
            if not page_token:
                break

        self.assertItemsEqual(expected, got)
        self.assertEquals(expected_pages, got_pages)

    def test_list_datasets_no_index(self):
        response = self.client.open(
            '/v1/datasets',
            method='GET',
            content_type='application/json')
        self.assertStatus(response, 200)
        self.assertEquals(response.json.get('datasets'), [])

    @parameterized.expand([
        param('negative', page_size=-33),
        param('zero', page_size=0),
        param('bad token', page_token='flaco'),
        param('good b64, bad JSON token',
              page_token=base64.urlsafe_b64encode(json.dumps({
                  'fox': 'mccloud'
              }))),
    ])
    def test_list_datasets_invalid_inputs(self, _, page_size=None,
                                          page_token=None):
        query_string = []
        if page_size is not None:
            query_string.append(('pageSize', page_size))
        if page_token is not None:
            query_string.append(('pageToken', page_token))
        response = self.client.open(
            '/v1/datasets',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assertStatus(response, 400)

    def test_create_dataset(self):
        ds = Dataset(name='datasets/foo')
        self.must_create_dataset(ds)

        got = self.must_get_dataset(ds.name)
        self.assertEqual(ds, got)

    def test_create_dataset_duplicate(self):
        ds = Dataset(name='datasets/foo')
        self.must_create_dataset(ds)

        resp = self.client.open(
            '/v1/datasets',
            method='POST',
            data=json.dumps(ds),
            content_type='application/json')
        self.assertStatus(resp, 409)

    def test_get_dataset_not_found(self):
        resp = self.client.open('/v1/datasets/foo', method='GET')
        self.assertStatus(resp, 404)

    def test_update_dataset(self):
        ds = Dataset(name='datasets/foo')
        self.must_create_dataset(ds)

        resp = self.client.open(
            '/v1/' + ds.name,
            method='PUT',
            data=json.dumps(ds),
            content_type='application/json')
        self.assertStatus(resp, 200)

    def test_update_dataset_not_found(self):
        resp = self.client.open(
            '/v1/datasets/notfound',
            method='PUT',
            data=json.dumps({
                'name': 'datasets/notfound'
            }),
            content_type='application/json')
        self.assertStatus(resp, 404)

    def test_update_dataset_mismatch_names(self):
        ds = Dataset(name='datasets/foo')
        self.must_create_dataset(ds)

        resp = self.client.open(
            '/v1/' + ds.name,
            method='PUT',
            data=json.dumps({
                'name': 'datasets/bar'
            }),
            content_type='application/json')
        self.assertStatus(resp, 400)

    def test_delete_dataset(self):
        ds = Dataset(name='datasets/foo')
        ds_untouched = Dataset(name='datasets/untouched')
        self.must_create_dataset(ds)
        self.must_create_dataset(ds_untouched)

        resp = self.client.open('/v1/' + ds.name, method='DELETE')
        self.assertStatus(resp, 200)
        resp = self.client.open('/v1/' + ds.name, method='GET')
        self.assertStatus(resp, 404)
        self.must_get_dataset(ds_untouched.name,
                              'unrelated dataset was deleted')

    def test_delete_dataset_not_found(self):
        ds_untouched = Dataset(name='datasets/untouched')
        self.must_create_dataset(ds_untouched)

        resp = self.client.open('/v1/datasets/notfound', method='DELETE')
        self.assertStatus(resp, 404)
        self.must_get_dataset(ds_untouched.name,
                              'unrelated dataset was deleted')


class TestExamplesInDocstrings(unittest.TestCase):
    """Test examples in doc strings."""

    def test_doctest(self):
        result = doctest.testmod(datasets_controller, report=True)
        self.assertEqual(0, result.failed)

if __name__ == '__main__':
    import unittest
    unittest.main()
