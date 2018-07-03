import os
from app.aeskeywrapper import AESKeyWrapper
from config import Config

config = Config()

wrapper = AESKeyWrapper(vault = config.azure_keyvault_url,
                        client_id = config.azure_service_principal_client_id,
                        secret = config.azure_service_principal_secret,
                        tenant = config.azure_tenant_id,
                        key_name = config.azure_keyvault_key_name,
                        key_version = config.azure_keyvault_key_version)

public_key = wrapper.get_public_key()

for i in range(100):
    key = os.urandom(config.aes_key_length)
    wrapped_key = wrapper.wrap_aes_key_local(key, public_key)
    restored_aes_key = wrapper.unwrap_aes_key(wrapped_key)
    if key != restored_aes_key:
        print("==========================")
        print(key)
        print("--------------------------")
        print(restored_aes_key)
        print("")
    else:
        print(i, "successful wrap & unwrap")
