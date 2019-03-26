from .aescipher import AESCipher
from .aeskeywrapper import AESKeyWrapper

import os

class Encryptor:

    @staticmethod
    def create_with_raw_key(vault, credentials, key_name, key_version, key=None, iv_length=16):
        return Encryptor(vault, credentials, key_name, key_version, key, iv_length)

    @staticmethod
    def create_with_wrapped_key(vault, credentials, key_name, key_version, wrapped_key, iv_length=16):
        encryptor = Encryptor(vault, credentials, key_name, key_version)
        encryptor._set_wrapped_key(wrapped_key, iv_length)
        return encryptor

    def __init__(self, vault, credentials, key_name, key_version, key=None, iv_length=16):
        self._wrapper = AESKeyWrapper(vault, credentials, key_name, key_version)
        if key is None:
            key = Encryptor.generate_aes_key()
        self._key = key
        self._iv_length = iv_length
        self._update_cipher()

    @staticmethod
    def generate_aes_key(length=32):
        return os.urandom(length)

    def _set_wrapped_key(self, wrapped_key, iv_length=None):
        self._key = self._wrapper.unwrap_aes_key(wrapped_key)
        if iv_length is not None:
            self._iv_length = iv_length
        self._update_cipher()

    def get_wrapped_key(self):
        return self._wrapper.wrap_aes_key_local(self._key, self._wrapper.get_public_key())

    def encrypt(self, data):
        return self._cipher.encrypt(data)

    def decrypt(self, data):
        return self._cipher.decrypt(data)

    def _update_cipher(self):
        self._cipher = AESCipher(self._key, self._iv_length)
