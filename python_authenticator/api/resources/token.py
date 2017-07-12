#!/usr/bin/env python
#
#   API Resource: TOKEN
#
#   Handles TOTP/HOTP token generation
#
#   v0.1 -- Marco Caimi <marco.caimi@fastweb.it>
#

from datetime import datetime
from time import time
import logging
from flask_restful import Resource
from flask import request
from python_authenticator.api.constants import API_DESCRIPTION, API_VENDOR, API_VERSION, API_ENDPOINT
from python_authenticator.api.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from python_authenticator import account_params_singleton

# import OTP library
import base64
try:
    from rfc6238 import totp
except ImportError as e:
    raise ImportError("Cannot import required module: [%s]" % e)

# class that will respond to the GET method of the 'token' api command
# http://endpoint:port/token/
class Token(Resource):
    __logger = logging.getLogger('TokenAPI')

    # returns list of all registered accounts
    def get(self):
        # response format
        TOKEN_RESPONSE_DICT = {
                'timestamp': ''
            }

        TOKEN_RESPONSE_DICT['timestamp'] = datetime.fromtimestamp(time()).__str__()
        registered_accounts = dict()
        for account in account_params_singleton.accounts.keys():
            acct = account_params_singleton.accounts.classes[account]
            registered_accounts[account] = {
                        'account': acct.account,
                        'type': acct.type,
                        'account_type': acct.account_type
                    }

        # fill account information in response json
        TOKEN_RESPONSE_DICT['accounts'] = registered_accounts

        return TOKEN_RESPONSE_DICT, HTTP_200_OK

    # get token for requested account
    def post(self):
        # response format
        TOKEN_RESPONSE_DICT = {
                'timestamp': ''
            }
        TOKEN_RESPONSE_DICT['timestamp'] = datetime.fromtimestamp(time()).__str__()

        # check request format and generate token
        if (request.is_json):
            try:
                account_string = request.json['account_string']
                token_type = request.json['token_type']
            except KeyError as e:
                return {'error': 'Body malformed.'}, HTTP_400_BAD_REQUEST

            if account_string in account_params_singleton.accounts.keys():
                account = account_params_singleton.accounts.classes[account_string]
                if token_type == "totp":
                    # get key
                    key = account.shared_secret
                    # compute token
                    if account.account_type == "google":
                        token_code = totp.TOTP(key, encode_base32=True)
                    else:
                        token_code = totp.TOTP(key, encode_base32=False)

                    TOKEN_RESPONSE_DICT['token'] = {
                            'account_string': account_string,
                            'account': account.account,
                            'account_type': account.account_type,
                            'token': token_code
                            }
                else:
                    return {'Token type [%s] is currently not supported.' & token_type}, HTTP_400_BAD_REQUEST
            else:
                return {'error': 'Account not found.'}, HTTP_200_OK

        else:
            return {'error': 'Malformed request: expected application/json'}, HTTP_400_BAD_REQUEST

        return TOKEN_RESPONSE_DICT, HTTP_200_OK


