#!/usr/bin/env python
#
# Python TOTP API Client
#

import sys
from argparse import ArgumentParser
import json

try:
    from requests import get, post
    from python_authenticator import config_params_singleton
    from python_authenticator.utils.ConsoleUtils import ANSIColors
except ImportError as e:
    print("Cannot Import Library Classes: [%s]" % e)
    sys.exit(-1)

arg_parser = ArgumentParser(prog="pytoken.py", epilog="Encrypt Everything!")
arg_parser.add_argument("--list", "-l", action="store_true")
options = arg_parser.parse_args()

# connect to the API endpoint
API_ENDPOINT = "http://%s:%s" % (config_params_singleton.apiserver.listen_address,
                                 config_params_singleton.apiserver.listen_port)
VERSION_PATH = "/api/"
TOKEN_PATH = "/token/"

console = ANSIColors()

if (options.list is True):
    results = get(API_ENDPOINT+TOKEN_PATH)
    if results.status_code == 200:
        retpayload = results.json()['accounts']
        for account in retpayload.keys():
            print("- '%s'" % console.warning(account))
            print("\tE-Mail: %s, type [%s]" % (retpayload[account]['account'], retpayload[account]['type']))
    else:
        print("Received error code [%d]. Bailing Out." % results.status_code)
else:
    results = get(API_ENDPOINT+TOKEN_PATH)
    if results.status_code == 200:
        retpayload = results.json()['accounts']
        for account in retpayload.keys():
            postresults = post(API_ENDPOINT+TOKEN_PATH,
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps({
                                        'account_string': account,
                                        'token_type': retpayload[account]['type']
                                        }
                                ))
            if postresults.status_code != 200:
                print("[------] Account %s rejected: Token type %s not yet supported." % (account, retpayload[account].get('type')))
            else:
                coderesults = postresults.json()['token']
                print("[%s] Account %s (%s)" % ((coderesults['token']), account, coderesults['account']))
    else:
        print("Received error code [%d]. Bailing Out." % results.status_code)
