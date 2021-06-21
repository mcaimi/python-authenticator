#
#   Base library configuration file
#   v0.1 -- Marco Caimi <mcaimi@redhat.com>
#

import sys
import logging

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())

from python_authenticator.utils import account_params_singleton, config_params_singleton

config_params = config_params_singleton
account_params = account_params_singleton

if config_params is not None:
    logging.basicConfig(filename=config_params.globals.log_file, level=logging.INFO)


