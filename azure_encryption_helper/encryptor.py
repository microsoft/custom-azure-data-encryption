from .aescipher import AESCipher
from .aeskeywrapper import AESKeyWrapper

import os

class Encryptor:

    def __init__(self, key=None, iv_length=16):
        if key is None:
            key = Encryptor.generate_aes_key()
        self.key = key
        self.iv_length = iv_length
        self._update_cipher()

    @staticmethod
    def generate_aes_key(length=32):
        return os.urandom(length)

    def configure_wrapper(self, vault, credentials, key_name, key_version):
        self.wrapper = AESKeyWrapper(vault, credentials, key_name, key_version)

    def set_key(self, key, iv_length=None):
        self.key = key
        if iv_length is not None:
            self.iv_length = iv_length
        self._update_cipher()

    def get_key(self, key):
        return self.key

    def set_wrapped_key(self, wrapped_key, iv_length=None):
        self.key = self.wrapper.unwrap_aes_key(wrapped_key)
        if iv_length is not None:
            self.iv_length = iv_length
        self._update_cipher()

    def get_wrapped_key(self):
        return self.wrapper.wrap_aes_key_local(self.key, self.wrapper.get_public_key())

    def encrypt(self, data):
        return self.cipher.encrypt(data)

    def decrypt(self, data):
        return self.cipher.decrypt(data)

    def _update_cipher(self):
        self.cipher = AESCipher(self.key, self.iv_length)
