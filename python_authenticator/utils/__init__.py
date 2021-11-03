#!/usr/bin/env python
from .ConfigParsers import AccountsParamsSingleton, ConfigParamsSingleton, NoOpParser

config_params_singleton = None
account_params_singleton = None
api_doc_singleton = None

# Load and parse service parameters from json file
try:
    config_params_singleton = ConfigParamsSingleton()
    config_params_singleton.parse()
    account_params_singleton = AccountsParamsSingleton()
    account_params_singleton.parse()
    api_doc_singleton = NoOpParser()
    api_doc_singleton.parse()
except Exception as e:
    print("libs.utils.__init__(): [%s]" % e.__str__())
    config_params_singleton = None
    account_params_singleton = None
    api_doc_singleton = None
