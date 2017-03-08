#!/usr/bin/env python
from setuptools import setup, find_packages

# install OTP modules
setup(
        name="python-authenticator",
        version="0.1",
        packages=find_packages(),
        author="Marco Caimi",
        author_email="marco.caimi@fastweb.it",
        description="Simple RESTful TOTP Authenticator for my linux desktop.",
        license="GPL v3",
        url="http://mi-ber-vlgit01.dev.fastcloud.fwb/mcaimi/python-authenticator.git"
)
