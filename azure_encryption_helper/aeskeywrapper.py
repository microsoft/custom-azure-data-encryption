from azure.keyvault import KeyVaultClient

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.primitives import hashes

class AESKeyWrapper:
    """ Wrapper for key wrapping functions.

    Key is wrapped localy with public key retrieved from Azure KeyVault.
    Uses Azure KeyVault API to unwrap the key.
    """

    def __init__(self, vault, credentials, key_name, key_version):
        """
        Wrapper constructor.

        :param str vault: Azure KeyVault url.
        :param str credentials: Credentials needed for the KV client to connect to Azure.
        :param str key_name: Azure KeyVault key name.
        :param str key_version: Azure KeyVault key version.
        """
        self._key_name = key_name
        self._key_version = key_version
        self._vault = vault
        self._credentials = credentials
        self.kvclient = KeyVaultClient(self._credentials)

    def wrap_aes_key_local(self, aes_key, public_key):
        """
        Wraps AES key locally.
        Uses RSA-OAEP algorithm to wrap provided key.

        :param str aes_key: unencrypted AES key.
        :param str public_key: public part of RSA key.

        :return: String with encrypted AES key.
        """
        int_n = self._bytes_to_int(public_key.n)
        int_e = self._bytes_to_int(public_key.e)
        public_numbers = RSAPublicNumbers(int_e, int_n)
        public_key = public_numbers.public_key(default_backend())

        wrapped_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None))
        return wrapped_key

    def unwrap_aes_key(self, wrapped_key):
        """
        Unwraps AES key with Azure KeyVault.
        Uses RSA-OAEP algorithm to unwrap provided key.

        :param str wrapped_key: encrypted AES key.

        :return: String with unencrypted AES key.
        """
        return self.kvclient.unwrap_key(
            self._vault,
            self._key_name,
            self._key_version,
            "RSA-OAEP",
            wrapped_key).result

    def get_public_key(self):
        """ Retrieve public key from Azure KeyVault.

        :return: JsonWebKey with public RSA key.
        """
        key_bundle = self.kvclient.get_key(self._vault, self._key_name, self._key_version)
        return key_bundle.key


    def _bytes_to_int(self, bytes):
        """ Helper function to convert bytes array to int. """
        result = 0
        for b in bytes:
            result = result * 256 + ord(b)
        return result
