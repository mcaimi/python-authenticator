#!/usr/bin/env python
# pylint: disable=R0903
#
#  v0.1 -- Caimi Marco <mcaimi@redhat.com>
#

"""  Configuration Parsing Metaclass. """

from os import path, environ
import json
from abc import ABCMeta, abstractmethod


class InnerMeta(metaclass=ABCMeta):
    """ Inner Component Metaclass Definition """

    def __init__(self, params_base):
        if params_base.__class__ is not dict:
            raise TypeError(f"InnerMeta: Type Mismatch: expected 'dict' instance, got {params_base.__class__}")

    @abstractmethod
    def parse(self):
        ''' object parsing abstract method '''
        raise NotImplementedError("InnerMeta.parse() BASE CLASS -  You have to derive and implement your own specialized version.")


class ParamsParser(metaclass=ABCMeta):
    """ Parameters Manage Metaclass Definition """

    def __init__(self, params_filename):
        try:
            self.homepath = environ['XDG_CONFIG_HOME']
        except KeyError as invalid_key_exception:
            raise invalid_key_exception

        # search the filesystem for the paramenters file
        valid_paths = [params_filename[i].replace('~', self.homepath) for i in params_filename.keys()]
        available_config_files = list(filter(path.exists, valid_paths))
        if len(available_config_files) == 0:
            raise Exception("ParamsParser: json config not found on filesystem")

        self.config_file = available_config_files[0]
        # read contents of the first file found on path.
        try:
            with open(self.config_file, 'r', encoding='utf-8') as json_file:
                self.raw_json = json.load(json_file)
        except Exception as json_error:
            raise json_error

    @abstractmethod
    def parse(self):
        ''' object parser abstract method '''
        raise NotImplementedError("ParamsParser.parse() BASE CLASS -  You have to derive and implement your own specialized version.")
