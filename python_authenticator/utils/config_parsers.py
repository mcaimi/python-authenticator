#!/usr/bin/env python
# pylint: disable=R0903
# pylint: disable=C0115
#
# v0.1 - Initial implementation - Marco Caimi <mcaimi@redhat.com>
#

''' Common utils for dealing with configuration files '''

from python_authenticator.config import parameters_json_file_source, api_spec_json_file_source, accounts_json_file_source
from python_authenticator.utils.parser_meta import ParamsParser, InnerMeta


class AccountParams(ParamsParser):
    """ Custom parser for account parameter config files """

    def __init__(self):
        super().__init__(accounts_json_file_source)
        self.service_classes = ['accounts']

    class InnerComponent(InnerMeta):
        """ Inner Component Implementation """

        def __init__(self, properties_hash):
            super().__init__(properties_hash)
            self.properties = properties_hash
            self.classes = {}
            self.parse()

        class JsonConfig(InnerMeta):
            """ JSON Handler Component Implementation """

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
            ''' return keys representing configuration parameters '''
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
            self.classes = {}
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
            raise RuntimeError("There can only be one instance of this class.")

        super().__init__(api_spec_json_file_source)
        self.json_data = None

        NoOpParser.__instance = self

    def parse(self):
        self.json_data = self.raw_json
