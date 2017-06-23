# coding: utf-8

from __future__ import absolute_import
from .base_model_ import Model
from datetime import date, datetime
from typing import List, Dict
from ..util import deserialize_model


class Dataset(Model):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, name=None):
        """
        Dataset - a model defined in Swagger

        :param name: The name of this Dataset.
        :type name: str
        """
        self.swagger_types = {
            'name': str
        }

        self.attribute_map = {
            'name': 'name'
        }

        self._name = name

    @classmethod
    def from_dict(cls, dikt):
        """
        Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Dataset of this Dataset.
        :rtype: Dataset
        """
        return deserialize_model(dikt, cls)

    @property
    def name(self):
        """
        Gets the name of this Dataset.
        Unique client-specified resource name of the form 'datasets/*'. 

        :return: The name of this Dataset.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Dataset.
        Unique client-specified resource name of the form 'datasets/*'. 

        :param name: The name of this Dataset.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

