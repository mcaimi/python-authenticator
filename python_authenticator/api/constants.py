#!/usr/bin/env python
#
#   Global repository for constants used across the API server
#   v0.1 -- Marco Caimi <mcaimi@redhat.com>
#

API_VERSION = "0.1"
API_VENDOR = "RedHat"
API_DESCRIPTION = "TOTP/HOTP Authenticator"
ENDPOINT = "localhost"
PORT = 5100
API_ENDPOINT = "http://%s:%s" % (ENDPOINT, PORT)
