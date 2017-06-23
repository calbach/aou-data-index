#!/usr/bin/env python

import connexion
from .encoder import JSONEncoder

if __name__ == '__main__':
  app = connexion.App(__name__, specification_dir='./swagger/')
  app.app.json_encoder = JSONEncoder
  app.add_api(
      'swagger.yaml',
      arguments={
          'title':
              'API for indexing curated datasets with user-defined labels, and searching that index.  Where possible this API follows [Google Cloud API design guidelines]( https://cloud.google.com/apis/design/), including the convention of using relative resource names to refer to resources. For example, an Individual may be addressed by `datasets/x/individuals/y`;, where the entirety is a resource name and `y`; is the resource ID.'
      })
  app.run(port=8080)
