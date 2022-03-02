#!/usr/bin/env python
#
#
#   v0.1 -- -Caimi Marco <mcaimi@redhat.com> -- Initial Implementation
#
""" Python TOTP Token Generator API Server """

# restful sdk for python
from flask import Flask
from flask_restful import Api

# API resources
from python_authenticator import config_params
from python_authenticator.api.router import Router

# initalize application
try:
    flask_server = Flask(__name__)
    api_server = Api(flask_server)

    # api routing hooks
    api_router = Router(api_server)
except Exception as general_fault:
    print(general_fault)

# start api server
if __name__ == "__main__":
    flask_server.run(host=config_params.apiserver.listen_address,
                     port=config_params.apiserver.listen_port,
                     debug=config_params.apiserver.debug)
