"""
    config.py only contains the configuration class
"""
import os
import json

class Config(object):
    """
    This class contains configuration parameters for all applications
    """
    def __init__(self, config_file="config/config.json"):
        with open(config_file, "rt") as conf:
            self.__dict__ = json.loads(conf.read())

    azure_tenant_id = ""
    azure_service_principal_client_id = ""
    azure_service_principal_secret = ""
    azure_keyvault_url = ""
    azure_keyvault_key_name = ""
    azure_keyvault_key_version = ""
    aes_key_length = 32
    aes_iv_length = 16