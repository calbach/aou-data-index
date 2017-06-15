#!/usr/bin/env python

import argparse
import connexion
from .encoder import JSONEncoder
from swagger_server.controllers import curated_data_index_controller


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--port', type=int, default=8080)
  parser.add_argument('--index_addr', type=str, default='http://localhost:9200')
  args = parser.parse_args()

  app = connexion.App(__name__, specification_dir='./swagger/')
  app.app.json_encoder = JSONEncoder
  app.add_api('swagger.yaml', arguments={'title': 'API for indexing curated datasets with user-defined labels, and searching that index.'})
  curated_data_index_controller.INDEX_ADDR = args.index_addr
  app.run(port=args.port)
