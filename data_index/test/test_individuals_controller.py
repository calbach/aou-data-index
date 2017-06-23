from __future__ import absolute_import

from swagger_server.models.individual import Individual
from swagger_server.test import BaseTestCase
from six import BytesIO
from flask import json


class TestIndividualsController(BaseTestCase):
    """Individuals integration tests."""

    def test_create_individual(self):
        body = Individual()
        response = self.client.open(
            '/v1/datasets/{datasetId}/individuals'.format(
                datasetId='datasetId_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assertStatus(response, 501,
                          "Response body is : " + response.data.decode('utf-8'))

    def test_get_individual(self):
        response = self.client.open(
            '/v1/datasets/{datasetId}/individuals/{individualId}'.format(
                datasetId='datasetId_example',
                individualId='individualId_example'),
            method='GET',
            content_type='application/json')
        self.assertStatus(response, 501,
                          "Response body is : " + response.data.decode('utf-8'))

    def test_update_individual(self):
        body = Individual()
        response = self.client.open(
            '/v1/datasets/{datasetId}/individuals/{individualId}'.format(
                datasetId='datasetId_example',
                individualId='individualId_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assertStatus(response, 501,
                          "Response body is : " + response.data.decode('utf-8'))

    def test_delete_individual(self):
        response = self.client.open(
            '/v1/datasets/{datasetId}/individuals/{individualId}'.format(
                datasetId='datasetId_example',
                individualId='individualId_example'),
            method='DELETE',
            content_type='application/json')
        self.assertStatus(response, 501,
                          "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
