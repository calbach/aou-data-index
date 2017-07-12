#!/usr/bin/env python

import connexion
from .encoder import JSONEncoder

app = connexion.App(__name__, specification_dir='./swagger/')
app.app.json_encoder = JSONEncoder
app.add_api(
    'swagger.yaml',
    arguments={
        'title':
        'API for indexing curated datasets with user-defined labels, and searching that index.  Where possible this API follows [Google Cloud API design guidelines]( https://cloud.google.com/apis/design/), including the convention of using relative resource names to refer to resources. For example, an Individual may be addressed by `datasets/x/individuals/y`;, where the entirety is a resource name and `y`; is the resource ID.'
    })


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--port', type=int, default=9190)
  parser.add_argument('--index_addr', type=str, required=True)
  args = parser.parse_args()

  app.app.config['INDEX_ADDR'] = args.index_addr
  app.run(host='0.0.0.0', port=args.port)
