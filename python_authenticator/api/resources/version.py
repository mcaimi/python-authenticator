#!/usr/bin/env python
# pylint: disable=R0201
#
"""   API Resource: VERSION

   Returns API version and information
"""
#   v0.1 -- Marco Caimi <mcaimi@redhat.com>
#

from datetime import datetime
from time import time
import logging
from flask_restful import Resource
from python_authenticator.api.constants import API_DESCRIPTION, API_VENDOR, API_VERSION, API_ENDPOINT
from python_authenticator.api.status import HTTP_200_OK
from python_authenticator.utils import API_DOC_SINGLETON


class Version(Resource):
    """ class that will respond to the GET method of the 'version' api command
        http://endpoint:port/
    """

    __logger = logging.getLogger('VersionAPI')

    def get(self):
        ''' get api response '''

        version_response_dict = {
            'version': API_VERSION,
            'description_string': API_DESCRIPTION,
            'vendor': API_VENDOR,
            'documentation': '',
            'timestamp': ''
        }

        version_response_dict['documentation'] = API_ENDPOINT + "/api/docs"
        version_response_dict['timestamp'] = datetime.fromtimestamp(time()).__str__()
        return version_response_dict, HTTP_200_OK


class Docs(Resource):
    """ class that will respond to the GET method of the 'version' api command
        http://endpoint:port/
    """
    __logger = logging.getLogger('DocsAPI')

    def get(self):
        ''' get api response '''

        version_response_dict = {
            'version': API_VERSION,
            'description_string': API_DESCRIPTION,
            'vendor': API_VENDOR,
            'documentation': '',
            'timestamp': ''
        }
        version_response_dict['documentation'] = API_DOC_SINGLETON.json_data
        version_response_dict['timestamp'] = datetime.fromtimestamp(time()).__str__()
        return version_response_dict, HTTP_200_OK
