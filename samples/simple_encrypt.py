import os
from app.aeskeywrapper import AESKeyWrapper
from app.aescipher import AESCipher
from config import Config

config = Config()

sample_data = 'hello custom data encryption!'
print('Original Unencrypted Data: ', sample_data)

wrapper = AESKeyWrapper(
    vault = config.azure_keyvault_url,
    client_id = config.azure_service_principal_client_id,
    secret = config.azure_service_principal_secret,
    tenant = config.azure_tenant_id,
    key_name = config.azure_keyvault_key_name,
    key_version = config.azure_keyvault_key_version)

# Generate AES Key
aes_key = os.urandom(config.aes_key_length)

# Encrypt AES Key
encrypted_keys = wrapper.wrap_aes_key_local(aes_key, wrapper.get_public_key())

# Encrypt Data
cipher = AESCipher(wrapper.unwrap_aes_key(encrypted_keys), config.aes_iv_length)
encrypted_data = cipher.encrypt(sample_data)

print('Encrypted Data: ', encrypted_data)

# Unencrypt Data
unencrypted_data = cipher.decrypt(encrypted_data)
print('Unencrypted Data: ', unencrypted_data)