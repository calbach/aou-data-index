import connexion
from swagger_server.models.cdr_data_pointer import CdrDataPointer
from swagger_server.models.cdr_dataset import CdrDataset
from swagger_server.models.cdr_individual import CdrIndividual
from swagger_server.models.cdr_list_datasets_response import CdrListDatasetsResponse
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime


def create_data_pointer(dataset_id, body):
    """
    create_data_pointer
    
    :param dataset_id: 
    :type dataset_id: str
    :param body: 
    :type body: dict | bytes

    :rtype: CdrDataPointer
    """
    if connexion.request.is_json:
        body = CdrDataPointer.from_dict(connexion.request.get_json())
    return 'do some magic!'


def create_dataset(body):
    """
    create_dataset
    
    :param body: 
    :type body: dict | bytes

    :rtype: CdrDataset
    """
    if connexion.request.is_json:
        body = CdrDataset.from_dict(connexion.request.get_json())
    return 'do some magic!'


def create_individual(dataset_id, body):
    """
    create_individual
    
    :param dataset_id: 
    :type dataset_id: str
    :param body: 
    :type body: dict | bytes

    :rtype: CdrIndividual
    """
    if connexion.request.is_json:
        body = CdrIndividual.from_dict(connexion.request.get_json())
    return 'do some magic!'


def delete_data_pointer(dataset_id, data_pointer_id):
    """
    delete_data_pointer
    
    :param dataset_id: 
    :type dataset_id: str
    :param data_pointer_id: 
    :type data_pointer_id: str

    :rtype: None
    """
    return 'do some magic!'


def delete_dataset(dataset_id):
    """
    delete_dataset
    
    :param dataset_id: 
    :type dataset_id: str

    :rtype: None
    """
    return 'do some magic!'


def delete_individual(dataset_id, individual_id):
    """
    delete_individual
    
    :param dataset_id: 
    :type dataset_id: str
    :param individual_id: 
    :type individual_id: str

    :rtype: None
    """
    return 'do some magic!'


def get_data_pointer(dataset_id, data_pointer_id):
    """
    get_data_pointer
    
    :param dataset_id: 
    :type dataset_id: str
    :param data_pointer_id: 
    :type data_pointer_id: str

    :rtype: CdrDataPointer
    """
    return 'do some magic!'


def get_dataset(dataset_id):
    """
    get_dataset
    
    :param dataset_id: 
    :type dataset_id: str

    :rtype: CdrDataset
    """
    return 'do some magic!'


def get_individual(dataset_id, individual_id):
    """
    get_individual
    
    :param dataset_id: 
    :type dataset_id: str
    :param individual_id: 
    :type individual_id: str

    :rtype: CdrIndividual
    """
    return 'do some magic!'


def list_datasets(page_size=None, page_token=None):
    """
    list_datasets
    
    :param page_size: 
    :type page_size: int
    :param page_token: 
    :type page_token: str

    :rtype: CdrListDatasetsResponse
    """
    return 'do some magic!'


def update_data_pointer(dataset_id, data_pointer_id, body):
    """
    update_data_pointer
    
    :param dataset_id: 
    :type dataset_id: str
    :param data_pointer_id: 
    :type data_pointer_id: str
    :param body: 
    :type body: dict | bytes

    :rtype: CdrDataPointer
    """
    if connexion.request.is_json:
        body = CdrDataPointer.from_dict(connexion.request.get_json())
    return 'do some magic!'


def update_dataset(dataset_id, body):
    """
    update_dataset
    
    :param dataset_id: 
    :type dataset_id: str
    :param body: 
    :type body: dict | bytes

    :rtype: CdrDataset
    """
    if connexion.request.is_json:
        body = CdrDataset.from_dict(connexion.request.get_json())
    return 'do some magic!'


def update_individual(dataset_id, individual_id, body):
    """
    update_individual
    
    :param dataset_id: 
    :type dataset_id: str
    :param individual_id: 
    :type individual_id: str
    :param body: 
    :type body: dict | bytes

    :rtype: CdrIndividual
    """
    if connexion.request.is_json:
        body = CdrIndividual.from_dict(connexion.request.get_json())
    return 'do some magic!'
