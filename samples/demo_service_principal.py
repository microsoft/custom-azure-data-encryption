import os
from azure_encryption_helper import Encryptor
from azure.common.credentials import ServicePrincipalCredentials


client_id = os.environ['AZURE_CLIENT_ID']
client_secret = os.environ['AZURE_CLIENT_SECRET']
tenant_id = os.environ['AZURE_TENANT_ID']
credentials = ServicePrincipalCredentials(client_id=client_id, 
                                          secret=client_secret,
                                          tenant=tenant_id)

vault_uri = os.environ['VAULT_URI']
key_name = os.environ['KEY_NAME']
key_version = os.environ.get('KEY_VERSION', '')

message = 'hello custom data encryption!'
print("Original message:" + message)

encryptor_a = Encryptor()
encryptor_a.configure_wrapper(vault_uri, credentials, key_name, key_version)

encrypted_message = encryptor_a.encrypt(message)
wrapped_key = encryptor_a.get_wrapped_key()
print("Encrypted message:" + str(encrypted_message))
print("Wrapped_key:" + str(wrapped_key))

print("Transferring wrapped key and encrypted message...")

encryptor_b = Encryptor()
encryptor_b.configure_wrapper(vault_uri, credentials, key_name, key_version)
encryptor_b.set_wrapped_key(wrapped_key)
decrypted_message = encryptor_b.decrypt(encrypted_message)

print("Decrypted message:" + decrypted_message)