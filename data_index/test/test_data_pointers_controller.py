from __future__ import absolute_import

from swagger_server.models.data_pointer import DataPointer
from swagger_server.test import BaseTestCase
from six import BytesIO
from flask import json


class TestDataPointersController(BaseTestCase):
    """DataPointers integration tests."""

    def test_create_data_pointer(self):
        body = DataPointer()
        response = self.client.open(
            '/v1/datasets/{datasetId}/dataPointers'.format(
                datasetId='datasetId_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assertStatus(response, 501,
                          "Response body is : " + response.data.decode('utf-8'))

    def test_get_data_pointer(self):
        response = self.client.open(
            '/v1/datasets/{datasetId}/dataPointers/{dataPointerId}'.format(
                datasetId='datasetId_example',
                dataPointerId='dataPointerId_example'),
            method='GET',
            content_type='application/json')
        self.assertStatus(response, 501,
                          "Response body is : " + response.data.decode('utf-8'))

    def test_update_data_pointer(self):
        body = DataPointer()
        response = self.client.open(
            '/v1/datasets/{datasetId}/dataPointers/{dataPointerId}'.format(
                datasetId='datasetId_example',
                dataPointerId='dataPointerId_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assertStatus(response, 501,
                          "Response body is : " + response.data.decode('utf-8'))

    def test_delete_data_pointer(self):
        response = self.client.open(
            '/v1/datasets/{datasetId}/dataPointers/{dataPointerId}'.format(
                datasetId='datasetId_example',
                dataPointerId='dataPointerId_example'),
            method='DELETE',
            content_type='application/json')
        self.assertStatus(response, 501,
                          "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
