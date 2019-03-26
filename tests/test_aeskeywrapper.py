import pytest

from azure_encryption_helper.aeskeywrapper import AESKeyWrapper

from mock import Mock
from os import urandom
import string
import cryptography

mock_vault_name = "mock_vault"
mock_key_name = "mock_key_name"
mock_key_version = "mock_key_version"
mock_service_principal_credentails = Mock()
mock_key_vault_client = Mock()

class MockAESKeyWrapper(AESKeyWrapper):
    def __init__(self, vault, key_name, key_version,
        mock_service_principal_credentails, mock_key_vault_client):

        self._key_name = key_name
        self._key_version = key_version
        self._vault = vault
        self._credentials = mock_service_principal_credentails
        self.kvclient = mock_key_vault_client

def test_get_public_key():
    mock_wrapper = MockAESKeyWrapper(mock_vault_name, mock_key_name,
        mock_key_version, mock_service_principal_credentails, mock_key_vault_client)

    mock_wrapper.get_public_key()
    mock_key_vault_client.get_key.assert_called_with(
        mock_vault_name,
        mock_key_name,
        mock_key_version)

def test_unwrap_aes_key():
    mock_wrapped_key = "mock_wrapped_key"
    mock_wrap_algorithm = "RSA-OAEP"

    mock_wrapper = MockAESKeyWrapper(mock_vault_name, mock_key_name,
        mock_key_version, mock_service_principal_credentails, mock_key_vault_client)

    mock_wrapper.unwrap_aes_key(mock_wrapped_key)
    mock_key_vault_client.unwrap_key.assert_called_with(mock_vault_name, mock_key_name,
        mock_key_version, mock_wrap_algorithm, mock_wrapped_key)

def test_wrap_aes_key_local():
    mock_aes_key = urandom(32)
    mock_public_key = Mock()
    mock_public_key.n = b"w1jcEfmxCTz5aB9wGg1Vl5K45VUm8Aj7+05sBarmrwbvC9BNjAqSySPmC2ajWSQGdmBs4xylKZjHKaXg5rxuNw=="
    mock_public_key.e = b"65537"
    mock_wrapper = MockAESKeyWrapper(mock_vault_name, mock_key_name, mock_key_version,
        mock_service_principal_credentails, mock_key_vault_client)

    assert mock_wrapper.wrap_aes_key_local(mock_aes_key, mock_public_key) != None