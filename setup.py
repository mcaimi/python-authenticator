#!/usr/bin/env python
# pylint: disable=R0801
""" Module Setup """
from setuptools import setup, find_packages

# install OTP modules
setup(name="python-authenticator",
      version="0.1",
      packages=find_packages(),
      author="Marco Caimi",
      author_email="mcaimi@redhat.com",
      description="Simple RESTful TOTP Authenticator for my linux desktop.",
      license="GPL v3",
      url="https://github.com/mcaimi/python-authenticator")
