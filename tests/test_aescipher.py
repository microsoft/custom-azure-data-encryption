import pytest
import os
import random

from azure_encryption_helper.aescipher import AESCipher

aes_key_length = 32
aes_iv_length = 16

def test_encrypted_msg_size():
    mock_content = "mock content"
    padding = len(mock_content) % aes_iv_length
    padding_size = aes_iv_length - padding
    expected_encrypted_content_length = aes_iv_length + padding_size + len(mock_content)

    mock_aes_key = os.urandom(aes_key_length)
    cipher = AESCipher(mock_aes_key, aes_iv_length)

    encrypted_mock_content = cipher.encrypt(mock_content)
    assert expected_encrypted_content_length == len(encrypted_mock_content)

def test_encrypt_decrypt():
    mock_content = "mock content"
    mock_aes_key = os.urandom(aes_key_length)

    cipher = AESCipher(mock_aes_key, aes_iv_length)
    encrypted_mock_content = cipher.encrypt(mock_content)

    assert mock_content == cipher.decrypt(encrypted_mock_content)
