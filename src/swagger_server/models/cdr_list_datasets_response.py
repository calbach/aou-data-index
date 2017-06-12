# coding: utf-8

from __future__ import absolute_import
from swagger_server.models.cdr_dataset import CdrDataset
from .base_model_ import Model
from datetime import date, datetime
from typing import List, Dict
from ..util import deserialize_model


class CdrListDatasetsResponse(Model):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, datasets=None, next_page_token=None):
        """
        CdrListDatasetsResponse - a model defined in Swagger

        :param datasets: The datasets of this CdrListDatasetsResponse.
        :type datasets: List[CdrDataset]
        :param next_page_token: The next_page_token of this CdrListDatasetsResponse.
        :type next_page_token: str
        """
        self.swagger_types = {
            'datasets': List[CdrDataset],
            'next_page_token': str
        }

        self.attribute_map = {
            'datasets': 'datasets',
            'next_page_token': 'next_page_token'
        }

        self._datasets = datasets
        self._next_page_token = next_page_token

    @classmethod
    def from_dict(cls, dikt):
        """
        Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The CdrListDatasetsResponse of this CdrListDatasetsResponse.
        :rtype: CdrListDatasetsResponse
        """
        return deserialize_model(dikt, cls)

    @property
    def datasets(self):
        """
        Gets the datasets of this CdrListDatasetsResponse.

        :return: The datasets of this CdrListDatasetsResponse.
        :rtype: List[CdrDataset]
        """
        return self._datasets

    @datasets.setter
    def datasets(self, datasets):
        """
        Sets the datasets of this CdrListDatasetsResponse.

        :param datasets: The datasets of this CdrListDatasetsResponse.
        :type datasets: List[CdrDataset]
        """

        self._datasets = datasets

    @property
    def next_page_token(self):
        """
        Gets the next_page_token of this CdrListDatasetsResponse.

        :return: The next_page_token of this CdrListDatasetsResponse.
        :rtype: str
        """
        return self._next_page_token

    @next_page_token.setter
    def next_page_token(self, next_page_token):
        """
        Sets the next_page_token of this CdrListDatasetsResponse.

        :param next_page_token: The next_page_token of this CdrListDatasetsResponse.
        :type next_page_token: str
        """

        self._next_page_token = next_page_token
