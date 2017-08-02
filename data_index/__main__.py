#!/usr/bin/env python

import argparse
import connexion
from .encoder import JSONEncoder

app = connexion.App(__name__, specification_dir='./swagger/')
app.app.json_encoder = JSONEncoder
app.add_api('swagger.yaml')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--port',
        type=int,
        default=9190,
        help='The port on which to serve HTTP requests')
    parser.add_argument(
        '--index_addr',
        type=str,
        required=True,
        help='The base URL address for the backend ElasticSearch index service')
    args = parser.parse_args()

    app.app.config['INDEX_ADDR'] = args.index_addr
    app.run(host='0.0.0.0', port=args.port)
else:
    # Require a config file env var for running with gunicorn.
    app.app.config.from_envvar('FLASK_SETTINGS')
