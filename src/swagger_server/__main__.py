#!/usr/bin/env python

import connexion
from .encoder import JSONEncoder


if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'API for indexing curated datasets with user-defined labels, and searching that index.'})
    app.run(port=8080)
