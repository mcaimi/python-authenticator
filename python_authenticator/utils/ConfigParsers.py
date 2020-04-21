#!/usr/bin/env python
#
# Python common utils for dealing with configuration files
#
# v0.1 - Initial implementation - Marco Caimi <mcaimi@redhat.com>
#

from os import _Environ
from os import path
import json

from python_authenticator.config import parameters_json_file_source, api_spec_json_file_source, accounts_json_file_source
from python_authenticator.utils.ParserMeta import ParamsParser, InnerMeta

# Custom parsers for parameter files
class AccountParams(ParamsParser):
    def __init__(self):
        super().__init__(accounts_json_file_source)
        self.service_classes = ['accounts']

    class InnerComponent(InnerMeta):
        def __init__(self, properties_hash):
            super().__init__(properties_hash)
            self.properties = properties_hash
            self.classes = {}
            self.parse()

        class JsonConfig(InnerMeta):
            def __init__(self, properties_hash):
                super().__init__(properties_hash)
                self.properties = properties_hash
                self.parse()

            def parse(self):
                for key in self.properties.keys():
                    setattr(self, key, self.properties[key])

        def parse(self):
            for key in self.properties.keys():
                self.classes[key] = self.JsonConfig(self.properties[key])

        def keys(self):
            return self.classes.keys()

    def parse(self):
        for service_class in self.service_classes:
            inner_element = self.InnerComponent(self.raw_json[service_class])
            setattr(self, service_class, inner_element)

# Custom parsers for parameter files
class ConfigParams(ParamsParser):
    def __init__(self):
        super().__init__(parameters_json_file_source)
        self.service_classes = ['apiserver', 'globals']

    class InnerComponent(InnerMeta):
        def __init__(self, properties_hash):
            super().__init__(properties_hash)
            self.properties = properties_hash
            self.classes = dict()
            self.parse()

        def parse(self):
            for key in self.properties.keys():
                setattr(self, key, self.properties[key])

    def parse(self):
        for service_class in self.service_classes:
            inner_element = self.InnerComponent(self.raw_json[service_class])
            setattr(self, service_class, inner_element)

# Custom parsers for parameter files
class ConfigParamsSingleton(ConfigParams):
    # Singleton handle
    __instance = None

    def __init__(self):
        if ConfigParamsSingleton.__instance is not None:
            raise RuntimeError("There can only be one instance of this class.")

        super().__init__()

        ConfigParamsSingleton._instance = self

# Custom parsers for parameter files
class AccountsParamsSingleton(AccountParams):
    # Singleton handle
    __instance = None

    def __init__(self):
        if AccountsParamsSingleton.__instance is not None:
            raise RuntimeError("There can only be one instance of this class.")

        super().__init__()

        AccountsParamsSingleton._instance = self

# Parser that loads the API spec json document
class NoOpParser(ParamsParser):
    __instance = None

    def __init__(self):
        if NoOpParser.__instance is not None:
            return NoOpParser.__instance

        super().__init__(api_spec_json_file_source)

        NoOpParser.__instance = self

    def parse(self):
        self.json_data = self.raw_json

