# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.cdr_data_pointer import CdrDataPointer
from swagger_server.models.cdr_dataset import CdrDataset
from swagger_server.models.cdr_individual import CdrIndividual
from swagger_server.models.cdr_list_datasets_response import CdrListDatasetsResponse
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestCuratedDataIndexController(BaseTestCase):
    """ CuratedDataIndexController integration test stubs """

    def test_create_data_pointer(self):
        """
        Test case for create_data_pointer

        
        """
        body = CdrDataPointer()
        response = self.client.open('/v1/datasets/{dataset_id}/dataPointers'.format(dataset_id='dataset_id_example'),
                                    method='POST',
                                    data=json.dumps(body),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_create_dataset(self):
        """
        Test case for create_dataset

        
        """
        body = CdrDataset()
        response = self.client.open('/v1/datasets',
                                    method='POST',
                                    data=json.dumps(body),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_create_individual(self):
        """
        Test case for create_individual

        
        """
        body = CdrIndividual()
        response = self.client.open('/v1/datasets/{dataset_id}/individuals'.format(dataset_id='dataset_id_example'),
                                    method='POST',
                                    data=json.dumps(body),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_delete_data_pointer(self):
        """
        Test case for delete_data_pointer

        
        """
        response = self.client.open('/v1/datasets/{dataset_id}/dataPointers/{data_pointer_id}'.format(dataset_id='dataset_id_example', data_pointer_id='data_pointer_id_example'),
                                    method='DELETE',
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_delete_dataset(self):
        """
        Test case for delete_dataset

        
        """
        response = self.client.open('/v1/datasets/{dataset_id}'.format(dataset_id='dataset_id_example'),
                                    method='DELETE',
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_delete_individual(self):
        """
        Test case for delete_individual

        
        """
        response = self.client.open('/v1/datasets/{dataset_id}/individuals/{individual_id}'.format(dataset_id='dataset_id_example', individual_id='individual_id_example'),
                                    method='DELETE',
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_get_data_pointer(self):
        """
        Test case for get_data_pointer

        
        """
        response = self.client.open('/v1/datasets/{dataset_id}/dataPointers/{data_pointer_id}'.format(dataset_id='dataset_id_example', data_pointer_id='data_pointer_id_example'),
                                    method='GET',
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_get_dataset(self):
        """
        Test case for get_dataset

        
        """
        response = self.client.open('/v1/datasets/{dataset_id}'.format(dataset_id='dataset_id_example'),
                                    method='GET',
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_get_individual(self):
        """
        Test case for get_individual

        
        """
        response = self.client.open('/v1/datasets/{dataset_id}/individuals/{individual_id}'.format(dataset_id='dataset_id_example', individual_id='individual_id_example'),
                                    method='GET',
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_list_datasets(self):
        """
        Test case for list_datasets

        
        """
        query_string = [('page_size', 56),
                        ('page_token', 'page_token_example')]
        response = self.client.open('/v1/datasets',
                                    method='GET',
                                    content_type='application/json',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_update_data_pointer(self):
        """
        Test case for update_data_pointer

        
        """
        body = CdrDataPointer()
        response = self.client.open('/v1/datasets/{dataset_id}/dataPointers/{data_pointer_id}'.format(dataset_id='dataset_id_example', data_pointer_id='data_pointer_id_example'),
                                    method='PUT',
                                    data=json.dumps(body),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_update_dataset(self):
        """
        Test case for update_dataset

        
        """
        body = CdrDataset()
        response = self.client.open('/v1/datasets/{dataset_id}'.format(dataset_id='dataset_id_example'),
                                    method='PUT',
                                    data=json.dumps(body),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_update_individual(self):
        """
        Test case for update_individual

        
        """
        body = CdrIndividual()
        response = self.client.open('/v1/datasets/{dataset_id}/individuals/{individual_id}'.format(dataset_id='dataset_id_example', individual_id='individual_id_example'),
                                    method='PUT',
                                    data=json.dumps(body),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
