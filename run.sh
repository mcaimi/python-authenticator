#!/bin/bash

ERRORLOG="python-authenticator.err"
(python /usr/local/bin/apiserver.py 2> /tmp/${ERRORLOG})&
