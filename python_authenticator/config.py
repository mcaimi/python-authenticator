#!/usr/bin/env python
""" main configuration files path definitions """

# possible locations for the configuration file placement on the local filesystem
parameters_json_file_source = {'primary': "parameters.json",
                               'alternate': "config/parameters.json",
                               'local': "~/parameters.json",
                               'system-wide': "/etc/python-authenticator/parameters.json"}

api_routing_json_file_source = {'primary': "api-routing.json",
                                'alternate': "config/api-routing.json",
                                'local': "~/api-routing.json",
                                'system-wide': "/etc/python-authenticator/api-routing.json"}

api_spec_json_file_source = {'primary': "api-methods.json",
                             'alternate': "config/api-methods.json",
                             'local': "~/api-methods.json",
                             'system-wide': "/etc/python-authenticator/api-methods.json"}

accounts_json_file_source = {'primary': "accounts.json",
                             'alternate': "accounts/accounts.json",
                             'local': "~/accounts/accounts.json"}
