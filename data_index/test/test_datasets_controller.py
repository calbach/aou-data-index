from __future__ import absolute_import

import doctest
import unittest
from data_index.controllers import datasets_controller
from data_index.models.dataset import Dataset
from data_index.models.list_datasets_response import ListDatasetsResponse
from data_index.test import BaseTestCase
from six import BytesIO
from flask import json


class TestDatasetsController(BaseTestCase):
    """Datasets tests."""

    def test_list_datasets(self):
        query_string = [('pageSize', 56), ('pageToken', 'pageToken_example')]
        response = self.client.open(
            '/v1/datasets',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assertStatus(response, 501,
                          "Response body is : " + response.data.decode('utf-8'))

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
                              "unrelated dataset was deleted")

    def test_delete_dataset_not_found(self):
        ds_untouched = Dataset(name='datasets/untouched')
        self.must_create_dataset(ds_untouched)

        resp = self.client.open('/v1/datasets/notfound', method='DELETE')
        self.assertStatus(resp, 404)
        self.must_get_dataset(ds_untouched.name,
                              "unrelated dataset was deleted")


class TestExamplesInDocstrings(unittest.TestCase):
    """Test examples in doc strings."""

    def test_doctest(self):
        result = doctest.testmod(datasets_controller, report=True)
        self.assertEqual(0, result.failed)

if __name__ == '__main__':
    import unittest
    unittest.main()
