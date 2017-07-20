from data_index.models.dataset import Dataset
from flask_testing import TestCase
from ..encoder import JSONEncoder
from flask import json
import connexion
import fake_elastic
import httpretty
import logging


class BaseTestCase(TestCase):
    INDEX_ADDR = 'http://localhost:123'

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../swagger/')
        app.app.json_encoder = JSONEncoder
        app.add_api('swagger.yaml')
        app.app.config.update({'INDEX_ADDR': BaseTestCase.INDEX_ADDR})
        return app.app

    def setUp(self):
        super(BaseTestCase, self).setUp()
        httpretty.enable()
        fake_elastic.register_httpretty(BaseTestCase.INDEX_ADDR,
                                        fake_elastic.FakeElastic())

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()
        super(BaseTestCase, self).tearDown()

    def must_create_dataset(self, ds):
        resp = self.client.open(
            '/v1/datasets',
            method='POST',
            data=json.dumps(ds),
            content_type='application/json')
        self.assertStatus(resp, 200)

    def must_get_dataset(self, name, desc=None):
        resp = self.client.open('/v1/' + name, method='GET')
        self.assertStatus(resp, 200, desc)
        return Dataset.from_dict(resp.json)

    def assertStatus(self, response, want, desc=None):
        if not desc:
            desc = 'Response body is : ' + response.data.decode('utf-8')
        super(BaseTestCase, self).assertStatus(response, want, desc)
