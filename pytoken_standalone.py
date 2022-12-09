#!/usr/bin/env python
# pylint: disable=C0301
# pylint: disable=E1101
#
# Python TOTP standalone command line interface
#
""" Python Authenticator CLI interface """

import sys
from argparse import ArgumentParser
import json
import hashlib
import binascii

SUPPORTED_CIPHERS: dict = {
                        "sha1": hashlib.sha1,
                        "sha256": hashlib.sha256,
                        "sha512": hashlib.sha512
                        }

try:
    from python_authenticator import ACCOUNT_PARAMS_SINGLETON
    from python_authenticator.utils.console_utils import ANSIColors
except ImportError as e:
    print(f"Cannot Import Library Classes: [{e}]")
    sys.exit(-1)

# import OTP library
try:
    from rfc6238 import totp
except ImportError as missing_totp_module:
    raise ImportError(f"Cannot import required module: [{missing_totp_module.__str__}]") from missing_totp_module

console: ANSIColors = ANSIColors()

def print_accounts_list(account_data_structure: dict) -> None:
    for account_id in account_data_structure.accounts.keys():
        json_data: dict = account_data_structure.accounts.classes[account_id]

        # Pre-format colored text output
        account_type: str = console.color_write(json_data.account_type, color="BLUE")
        account_name: str = console.color_write(json_data.account, color="RED")
        totp_type: str = console.color_write(json_data.type, color="YELLOW")

        # Print registered accounts
        print(f"[{account_type}] Account ID: {account_name} (type: {totp_type})")

def generate_totp_for_all_accounts(account_data_structure: dict) -> list:
    tokens = []
    for account in account_data_structure.accounts.keys():
        json_data: dict = account_data_structure.accounts.classes[account]

        try:
            # get account parameters
            shared_key: str = json_data.shared_secret
            base32: bool = json_data.base32
            digest_algorithm: Callable = SUPPORTED_CIPHERS.get(json_data.digest)

            # compute token value
            token_value: str = totp.totp(shared_key, digest=digest_algorithm, encode_base32=base32)

            # push computed token data to the tokens list
            tokens.append({'account': json_data.account, 'token': token_value})
        except binascii.Error as encoding_error:
            raise binascii.Error(f"Cannot process request for TOTP: [{encoding_error.__str__()}], key: {account}") from encoding_error
        except KeyError as missing_data_in_account_definition:
            raise KeyError(f"Cannot process request for TOTP: [{missing_data_in_account_definition.__str__()}]") from missing_data_in_account_definition

    # return token list
    return tokens

def display_tokens(tokens: list) -> None:
    for token_data in tokens:
        account_name: str = console.color_write(token_data.get('account'), color="YELLOW")
        token_value: str = console.color_write(token_data.get('token'), color="GREEN")

        # display entry
        print(f"[{token_value}] - Account ID: {account_name}")

def main() -> None:
    arg_parser: ArgumentParser = ArgumentParser(prog="pytoken.py", epilog="Standalone Version")
    arg_parser.add_argument("--list", "-l", action="store_true")
    options: dict = arg_parser.parse_args()

    if options.list:
        print_accounts_list(ACCOUNT_PARAMS_SINGLETON)
    else:
        tokens: list = generate_totp_for_all_accounts(ACCOUNT_PARAMS_SINGLETON)
        display_tokens(tokens)

# run script
main()
