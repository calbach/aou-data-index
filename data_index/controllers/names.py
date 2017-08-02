def split_individual_name(name):
  parts = name.split('/')
  if len(parts) != 4 or parts[0] != 'datasets' or parts[2] != 'individuals':
    raise BadRequest('malformed individual name "{}"'.format(name))
  return (parts[1], parts[3])


def data_pointer_name(ds_id, uri):
  id = urllib.quote(uri, safe='')
  return ('/datasets/{}/dataPointers/{}'.format(ds_id, id), id)
