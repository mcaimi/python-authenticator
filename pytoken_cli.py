#!/usr/bin/env python
# pylint: disable=C0301
# pylint: disable=E1101
#
# Python TOTP API Client
#
""" Python Authenticator CLI interface """

import sys
from argparse import ArgumentParser
import json

try:
    from requests import get, post
    from python_authenticator import CONFIG_PARAMS_SINGLETON
    from python_authenticator.utils.console_utils import ANSIColors
except ImportError as e:
    print(f"Cannot Import Library Classes: [{e}]")
    sys.exit(-1)

arg_parser = ArgumentParser(prog="pytoken.py", epilog="Encrypt Everything!")
arg_parser.add_argument("--list", "-l", action="store_true")
options = arg_parser.parse_args()

# connect to the API endpoint
API_ENDPOINT = f"http://{CONFIG_PARAMS_SINGLETON.apiserver.listen_address}:{CONFIG_PARAMS_SINGLETON.apiserver.listen_port}"
VERSION_PATH = "/api/"
TOKEN_PATH = "/token/"

console = ANSIColors()

if options.list is True:
    results = get(API_ENDPOINT + TOKEN_PATH)
    if results.status_code == 200:
        retpayload = results.json()['accounts']
        for account in retpayload.keys():
            print(f"- '{console.warning(account)}'")
            print(f"\tE-Mail: {retpayload[account]['account']} type [{retpayload[account]['type']}]")
    else:
        print(f"Received error code [{results.status_code}]. Bailing Out.")
else:
    results = get(API_ENDPOINT + TOKEN_PATH)
    if results.status_code == 200:
        retpayload = results.json()['accounts']
        for account in retpayload.keys():
            postresults = post(API_ENDPOINT + TOKEN_PATH,
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps({'account_string': account,
                                                'token_type': retpayload[account]['type']
                                                }))
            if postresults.status_code != 200:
                print(f"[------] Account {account} rejected: Token type {retpayload[account].get('type')} not yet supported.")
            else:
                coderesults = postresults.json()['token']
                print(f"[{coderesults['token']}] Account {account} ({coderesults['account']})")
    else:
        print(f"Received error code [{results.status_code}]. Bailing Out.")
