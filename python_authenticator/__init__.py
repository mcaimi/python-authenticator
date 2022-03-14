# pylint: disable=R0801
# pylint: disable=E1101
#
#   Base library configuration file
#   v0.1 -- Marco Caimi <mcaimi@redhat.com>
#
""" main python_authenticator module """

import logging
from python_authenticator.utils import ACCOUNT_PARAMS_SINGLETON, CONFIG_PARAMS_SINGLETON

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        """ placeholder class for null loggoing handler """

        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())

config_params = CONFIG_PARAMS_SINGLETON
account_params = ACCOUNT_PARAMS_SINGLETON

if config_params is not None:
    logging.basicConfig(filename=config_params.globals.log_file, level=logging.INFO)
