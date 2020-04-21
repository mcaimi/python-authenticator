#!/usr/bin/env python
# 
# Utility API decorators
#
# v0.1 -- Marco Caimi <mcaimi@redhat.com>
#
from functools import wraps
from flask import request
from python_authenticator.api.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST

MANDATORY_HEADERS = ['X-Auth-Token']

# parameters sanity check
def checkMandatoryParameters(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        truth_values = list(map(lambda x: x in request.headers.keys(), MANDATORY_HEADERS))
        if False in truth_values:
            return {'error': 'Missing Mandatory Parameter'}, HTTP_400_BAD_REQUEST
        else:
            return function(*args, **kwargs)
    return decorated_function

