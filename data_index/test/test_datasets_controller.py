from __future__ import absolute_import

from swagger_server.models.dataset import Dataset
from swagger_server.models.list_datasets_response import ListDatasetsResponse
from swagger_server.test import BaseTestCase
from six import BytesIO
from flask import json


class TestDatasetsController(BaseTestCase):
    """Datasets integration tests."""

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
        body = Dataset()
        response = self.client.open(
            '/v1/datasets',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assertStatus(response, 501,
                          "Response body is : " + response.data.decode('utf-8'))

    def test_get_dataset(self):
        response = self.client.open(
            '/v1/datasets/{datasetId}'.format(datasetId='datasetId_example'),
            method='GET',
            content_type='application/json')
        self.assertStatus(response, 501,
                          "Response body is : " + response.data.decode('utf-8'))

    def test_update_dataset(self):
        body = Dataset()
        response = self.client.open(
            '/v1/datasets/{datasetId}'.format(datasetId='datasetId_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assertStatus(response, 501,
                          "Response body is : " + response.data.decode('utf-8'))

    def test_delete_dataset(self):
        response = self.client.open(
            '/v1/datasets/{datasetId}'.format(datasetId='datasetId_example'),
            method='DELETE',
            content_type='application/json')
        self.assertStatus(response, 501,
                          "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
