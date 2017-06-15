from werkzeug.exceptions import NotFound

class DatasetNotFound(NotFound):
  def __init__(self, dataset_id, **kwargs):
    NotFound.__init__(self, '"datasets/{}" not found'.format(dataset_id), **kwargs)

class DataPointerNotFound(NotFound):
  def __init__(self, dataset_id, dp_id, **kwargs):
    NotFound.__init__(self, '"datasets/{}/dataPointers/{}" not found'.format(dataset_id, dp_id), **kwargs)

class IndividualNotFound(NotFound):
  def __init__(self, dataset_id, ind_id, **kwargs):
    NotFound.__init__(self, '"datasets/{}/individuals/{}" not found'.format(dataset_id, ind_id), **kwargs)
