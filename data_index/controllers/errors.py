from werkzeug.exceptions import NotFound

class DatasetNotFound(NotFound):
  def __init__(self, dataset_id, **kwargs):
    NotFound.__init__(self, '"datasets/{}" not found'.format(dataset_id), **kwargs)
