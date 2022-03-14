#!/usr/bin/env python
# Utility API decorators
#
# v0.1 -- Marco Caimi <mcaimi@redhat.com>
#
""" Function Decorators Definition """

from functools import wraps
from typing import Callable
from flask import request
from python_authenticator.api.status import HTTP_400_BAD_REQUEST

MANDATORY_HEADERS = ['X-Auth-Token']


def check_mandatory_parameters(function: Callable) -> Callable:
    """ Decorator that performs sanity checks.
        The decorated function is first checked for the presence of mandatory HTTP headers
        before being run
    """

    @wraps(function)
    def decorated_function(*args, **kwargs):
        truth_values = list(map(lambda x: x in request.headers.keys(), MANDATORY_HEADERS))
        if False in truth_values:
            return {'error': 'Missing Mandatory Parameter'}, HTTP_400_BAD_REQUEST
        return function(*args, **kwargs)
    return decorated_function
