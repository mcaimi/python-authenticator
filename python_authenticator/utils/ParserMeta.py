#!/usr/bin/env python
#
#  Configuration Parsing Metaclass.
#  v0.1 -- Caimi Marco <marco.caimi@fastweb.it
#

from os import path, environ
import json
from abc import ABCMeta, abstractmethod

# inner component base class
class InnerMeta(metaclass=ABCMeta):
    def __init__(self, params_base):
        if params_base.__class__ is not dict:
            raise TypeError("InnerMeta: Type Mismatch: expected 'dict' instance, got %s" % params_base.__class__)

    @abstractmethod
    def parse():
        raise NotImplementedError("InnerMeta.parse() BASE CLASS -  You have to derive and implement your own specialized version.")

# Parameters Handling Base Class 
class ParamsParser(metaclass=ABCMeta):
    def __init__(self, PARAMS_FILENAME):
        try:
            self.homepath = environ['XDG_CONFIG_HOME']
        except KeyError as e:
            raise e

        # search the filesystem for the paramenters file
        valid_paths = [PARAMS_FILENAME[i].replace('~', self.homepath) for i in PARAMS_FILENAME.keys()]
        available_config_files = list(filter(lambda x: path.exists(x), valid_paths))
        if len(available_config_files) == 0:
            raise Exception("ParamsParser: json config not found on filesystem")

        self.config_file = available_config_files[0]
        # read contents of the first file found on path.
        try:
            with open(self.config_file, 'r') as json_file:
                self.raw_json = json.load(json_file)
        except Exception as json_error:
            raise json_error

    # interface method
    @abstractmethod
    def parse():
        raise NotImplementedError("ParamsParser.parse() BASE CLASS -  You have to derive and implement your own specialized version.")

