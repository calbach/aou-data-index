#!/usr/bin/env python

import argparse
import connexion
import os
from swagger_server.controllers import es_proxy
from .encoder import JSONEncoder

app = connexion.App(__name__, specification_dir='./swagger/')
app.app.json_encoder = JSONEncoder
app.add_api('swagger.yaml', arguments={'title': 'API for indexing curated datasets with user-defined labels, and searching that index.'})
if __name__ != '__main__':
  # Require a config file env var for running with gunicorn.
  app.app.config.from_envvar('FLASK_SETTINGS')
app.app.register_blueprint(es_proxy.proxy)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--port', type=int, default=8080)
  parser.add_argument('--index_addr', type=str, default='http://localhost:9200')
  args = parser.parse_args()

  app.app.config['INDEX_ADDR'] = args.index_addr
  app.run(port=args.port)
