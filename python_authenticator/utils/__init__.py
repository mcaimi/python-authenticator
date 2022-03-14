#!/usr/bin/env python
# pylint: disable=W0703
""" Utility module for python_authenticator """

from .config_parsers import AccountsParamsSingleton, ConfigParamsSingleton, NoOpParser

# Load and parse service parameters from json file
try:
    CONFIG_PARAMS_SINGLETON = ConfigParamsSingleton()
    CONFIG_PARAMS_SINGLETON.parse()
    ACCOUNT_PARAMS_SINGLETON = AccountsParamsSingleton()
    ACCOUNT_PARAMS_SINGLETON.parse()
    API_DOC_SINGLETON = NoOpParser()
    API_DOC_SINGLETON.parse()
except Exception as e:
    print(f"libs.utils.__init__(): [{e.__str__()}]")
    CONFIG_PARAMS_SINGLETON = None
    ACCOUNT_PARAMS_SINGLETON = None
    API_DOC_SINGLETON = None
