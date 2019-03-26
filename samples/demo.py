import os
from azure_encryption_helper import Encryptor


# Create ServicePrincipalCredentials object using your SP
# You can use MSIAuthentication if running on Azure VM
if 'USE_MSI' in os.environ.keys():
    from msrestazure.azure_active_directory import MSIAuthentication
    credentials = MSIAuthentication(resource='https://vault.azure.net')
else:
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

# Create Encryptor
# credentials can be ServicePrincipalCrendentials or MSIAuthentication object
encryptor_a = Encryptor.create_with_raw_key(vault_uri, credentials, key_name, key_version)

# Encrypt messages
encrypted_message = encryptor_a.encrypt(message)

# Wrap AES key using RSA key from the KeyVault.
# Note that wrap operation is local, but it requires KV access to retrieve public part 
# of RSA key
wrapped_key = encryptor_a.get_wrapped_key()
print("Encrypted message:" + str(encrypted_message))
print("Wrapped_key:" + str(wrapped_key))

# Transfer message & key to the different location
print("Transferring wrapped key and encrypted message...")

# Create another Encryptor
encryptor_b = Encryptor.create_with_wrapped_key(vault_uri, credentials, key_name, key_version, wrapped_key)

# Now you can decrypt the message
decrypted_message = encryptor_b.decrypt(encrypted_message)
print("Decrypted message:" + decrypted_message)