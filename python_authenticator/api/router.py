#!/usr/bin/env python
# pylint: disable=R0903,E1101
#
#   v0.1 -- Caimi Marco <mcaimi@redhat.com>
#

""" API Router Implementation Code """

import logging
from importlib import import_module, invalidate_caches
from flask_restful import Api
from python_authenticator.utils.parser_meta import ParamsParser

from python_authenticator.config import api_routing_json_file_source as API_ROUTES


class ApiRouterConfig(ParamsParser):
    ''' Custom API routing configuration file parser class '''

    def __init__(self):
        super().__init__(API_ROUTES)
        self.root_objects = ['api']
        self.logger = logging.getLogger('ApiRouterConfig')
        self.logger.info("Loading api routes from %s", self.config_file)

    def parse(self):
        ''' load endpoint-object mappings as dictionary '''
        for json_root in self.root_objects:
            setattr(self, json_root, self.raw_json[json_root])


class Router():
    ''' The API call router. this class routes incoming requests to the corresponding handler class '''

    def __init__(self, api_server):
        if isinstance(api_server, Api):
            self.apiserver = api_server
            self.routes = ApiRouterConfig()
            self.routes.parse()
        else:
            raise TypeError("api_server must be of type flask_restful.Api")

        self.logger = logging.getLogger('APIRouter')
        self.route_endpoints()

    def route_endpoints(self):
        """ Route endpoint call to relevant object """

        for uri_path in self.routes.api.keys():
            self.logger.info("Attaching Endpoint '%s' to Handler Object '%s'.", uri_path, self.routes.api[uri_path])

            import_namespace = "python_authenticator.api.resources."
            class_name = self.routes.api[uri_path].split(":")[1]
            module_name = import_namespace + self.routes.api[uri_path].split(":")[0]
            self.logger.info(module_name)

            try:
                # load API handler module
                handler_module = import_module(module_name)
                invalidate_caches()
                handler_class = getattr(handler_module, class_name)
                self.apiserver.add_resource(handler_class, uri_path)
            except ImportError as import_error:
                self.logger.error(import_error)
            except Exception as generic_excp:
                self.logger.error(generic_excp)
