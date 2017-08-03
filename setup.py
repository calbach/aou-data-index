# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "data_index"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="Curated Data Index",
    author_email="",
    url="",
    keywords=["Swagger", "Curated Data Index"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    long_description="""\
    API for indexing curated datasets with user-defined labels, and searching that index.  Where possible this API follows [Google Cloud API design guidelines](https://cloud.google.com/apis/design/), including the convention of using relative resource names to refer to resources. For example, an Individual may be addressed by 'datasets/x/individuals/y';, where the entirety is a resource name 'y'; is the resource ID.
    """
)
