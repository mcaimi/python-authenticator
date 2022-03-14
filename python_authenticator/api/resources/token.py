#!/usr/bin/env python
# pylint: disable=E1101
# pylint: disable=R0201
#
"""
   API Resource: TOKEN

   Handles TOTP/HOTP token generation
"""
#   v0.1 -- Marco Caimi <mcaimi@redhat.com>
#

from datetime import datetime
import hashlib
from time import time
import logging
from flask_restful import Resource
from flask import request
from python_authenticator.api.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from python_authenticator import ACCOUNT_PARAMS_SINGLETON
from python_authenticator import config_params

# import OTP library
try:
    from rfc6238 import totp
except ImportError as missing_totp_module:
    raise ImportError(f"Cannot import required module: [{missing_totp_module.__str__}]") from missing_totp_module

SUPPORTED_CIPHERS = {"sha1": hashlib.sha1,
                     "sha256": hashlib.sha256,
                     "sha512": hashlib.sha512}


class Token(Resource):
    """ class that will respond to the GET method of the 'token' api command
        http://endpoint:port/token/
    """
    __logger = logging.getLogger('TokenAPI')

    def get(self):
        ''' returns list of all registered accounts '''

        token_response_dict = {'timestamp': ''}

        token_response_dict['timestamp'] = datetime.fromtimestamp(time()).__str__()
        registered_accounts = {}
        for account in ACCOUNT_PARAMS_SINGLETON.accounts.keys():
            acct = ACCOUNT_PARAMS_SINGLETON.accounts.classes[account]
            registered_accounts[account] = {'account': acct.account,
                                            'type': acct.type,
                                            'account_type': acct.account_type}

        # fill account information in response json
        token_response_dict['accounts'] = registered_accounts

        return token_response_dict, HTTP_200_OK

    def post(self):
        ''' get token for requested account '''

        # response format
        token_response_dict = {'timestamp': ''}
        token_response_dict['timestamp'] = datetime.fromtimestamp(time()).__str__()

        # check request format and generate token
        if request.is_json:
            try:
                account_string = request.json['account_string']
                token_type = request.json['token_type']
            except KeyError:
                return {'error': 'Body malformed.'}, HTTP_400_BAD_REQUEST

            if account_string in ACCOUNT_PARAMS_SINGLETON.accounts.keys():
                account = ACCOUNT_PARAMS_SINGLETON.accounts.classes[account_string]
                if token_type == "totp":
                    # get key
                    key = account.shared_secret
                    try:
                        digest_algo = SUPPORTED_CIPHERS.get(account.digest)
                        # compute token
                        token_code = totp.totp(key, digest=digest_algo, encode_base32=account.base32)
                    except KeyError:
                        token_code = 0

                    token_response_dict['token'] = {'account_string': account_string,
                                                    'account': account.account,
                                                    'account_type': account.account_type,
                                                    'issuer': account.issuer,
                                                    'token': token_code,
                                                    'provisioning_uri': totp.build_uri(key, account.account, account.issuer, account.digest, digits=config_params.globals.digits, period=config_params.globals.period)}
                else:
                    return {'error': f'Token type [{token_type}] is currently not supported.'}, HTTP_400_BAD_REQUEST
            else:
                return {'error': 'Account not found.'}, HTTP_200_OK

        else:
            return {'error': 'Malformed request: expected application/json'}, HTTP_400_BAD_REQUEST

        return token_response_dict, HTTP_200_OK
