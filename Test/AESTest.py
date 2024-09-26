import unittest
from src.Logic.AES_logic import AES, encrypt, decrypt

class AESTest(unittest.TestCase):

    def test_encrypt_correctly(self):
        message = b'Hello World12345'
        key = b'mysecretkey12345'
        ciphertext = AES(bytes(key)).encrypt_block(bytes(message))
        expected_ciphertext = b'\xf8\xc6\xdbO.\xd1\xc7\x8b\xa3\x19DX+\x1f^4'
        self.assertEqual(ciphertext, expected_ciphertext)

    """
    Tests encrypt and decryption using 192- and 256-bit keys.
    """
    def test_192(self):
        key = (b'B' * 24)
        aes = AES(key)
        message = b'Hello World12345'
        ciphertext = aes.encrypt_block(message)
        self.assertEqual(aes.decrypt_block(ciphertext), message)

    def test_256(self):
        key = (b'B' * 32)
        aes = AES(key)
        message = b'Hello World12345'
        ciphertext = aes.encrypt_block(message)
        self.assertEqual(aes.decrypt_block(ciphertext), message)

    def test_long_message(self):
        """ CBC should allow for messages longer than a single block. """
        long_message = b'M' * 100
        ciphertext = self.AES.encrypt_pcbc(long_message, self.iv)
        self.assertEqual(self.AES.decrypt_pcbc(ciphertext, self.iv), long_message)