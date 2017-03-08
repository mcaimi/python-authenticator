#!/usr/bin/env python
#
#   API Resource: VERSION
#
#   Returns API version and information
#
#   v0.1 -- Marco Caimi <marco.caimi@fastweb.it>
#

from datetime import datetime
from time import time
import logging
from flask_restful import Resource
from flask import request
from python_authenticator.api.constants import API_DESCRIPTION, API_VENDOR, API_VERSION, API_ENDPOINT
from python_authenticator.api.status import HTTP_200_OK
from python_authenticator.utils import api_doc_singleton

# class that will respond to the GET method of the 'version' api command
# http://endpoint:port/
class Version(Resource):
    __logger = logging.getLogger('VersionAPI')

    def get(self):
        # response format
        VERSION_RESPONSE_DICT = {
            'version': API_VERSION,
            'description_string': API_DESCRIPTION,
            'vendor': API_VENDOR,
            'documentation': '',
            'timestamp': ''
        }

        VERSION_RESPONSE_DICT['documentation'] = API_ENDPOINT + "/api/docs"
        VERSION_RESPONSE_DICT['timestamp'] = datetime.fromtimestamp(time()).__str__()
        return VERSION_RESPONSE_DICT, HTTP_200_OK

# class that will respond to the GET method of the 'version' api command
# http://endpoint:port/
class Docs(Resource):
    __logger = logging.getLogger('DocsAPI')

    def get(self):
        # response format
        VERSION_RESPONSE_DICT = {
            'version': API_VERSION,
            'description_string': API_DESCRIPTION,
            'vendor': API_VENDOR,
            'documentation': '',
            'timestamp': ''
        }
        VERSION_RESPONSE_DICT['documentation'] = api_doc_singleton.json_data
        VERSION_RESPONSE_DICT['timestamp'] = datetime.fromtimestamp(time()).__str__()
        return VERSION_RESPONSE_DICT, HTTP_200_OK

