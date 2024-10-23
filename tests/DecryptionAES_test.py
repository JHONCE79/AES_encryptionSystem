import unittest

import sys
sys.path.append("src")

from EncryptionSystem import AES_logic
from EncryptionSystem.AES_logic import encrypt, decrypt

class DecryptionAESTest(unittest.TestCase):
    # Normal cases
    def test_decrypt_correctly(self):
        plaintext = b'kHETYJEm1cua9mGD0C3YDZ2YsctWunTX4r4WhA5pBSQ='
        key = "mysecretkey12345"
        encrypted_message = encrypt(key, plaintext)
        decrypted_message = decrypt(key, encrypted_message)
        self.assertEqual(decrypted_message, plaintext)

    def test_decrypt_short_message(self):
        plaintext = b'9nteaA4XTc1Jg1aP0N334NxBtiyFi0DrfcZ6HjLNHc='
        key = "mysecretkey12345"
        encrypted_message = encrypt(key, plaintext)
        decrypted_message = decrypt(key, encrypted_message)
        self.assertEqual(decrypted_message, plaintext)

    def test_decrypt_message_512_bits(self):
        plaintext = b'Vn4JgjeUK6Ee4MCIPseJSEGjuMM6mHLAGlYaqdR[685 chars]QA=='
        key = "mysecretkey12345"
        encrypted_message = encrypt(key, plaintext)
        decrypted_message = decrypt(key, encrypted_message)
        self.assertEqual(decrypted_message, plaintext)

    #Special cases
    def test_decrypt_special_characters(self):
        plaintext = b'QWERTY1234567890!@#$%^&*()'
        key = "mysecretkey12345"
        encrypted_message = encrypt(key, plaintext)
        decrypted_message = decrypt(key, encrypted_message)
        self.assertEqual(decrypted_message, plaintext)

    def test_decrypt_long_message(self):
        plaintext = b'Vn4JgjeUK6Ee4MCIPseJSEGjuMM6mHLAGlYaqdR[685 chars]QA==Vn4JgjeUK6Ee4MCIPseJSEGjuMM6mHLAGlYaqdR[685 chars]QA==Vn4JgjeUK6Ee4MCIPseJSEGjuMM6mHLAGlYaqdR[685 chars]QA==Vn4JgjeUK6Ee4MCIPseJSEGjuMM6mHLAGlYaqdR[685 chars]QA=='
        key = "mysecretkey12345"
        encrypted_message = encrypt(key, plaintext)
        decrypted_message = decrypt(key, encrypted_message)
        self.assertEqual(decrypted_message, plaintext)

    def test_decrypt_message_numbers(self):
        plaintext = b'425365312345678904363845232543'
        key = "mysecretkey12345"
        encrypted_message = encrypt(key, plaintext)
        decrypted_message = decrypt(key, encrypted_message)
        self.assertEqual(decrypted_message, plaintext)

    #Error cases

    def test_decrypt_incorrect_key(self):
        plaintext = "mywrongkey123456"
        key = "mywrongkey123456"
        if plaintext != key: 
            with self.assertRaises(AES_logic.IncorrectKey):
                decrypt(key, plaintext)


    def test_decrypt_empty_ciphertext_error(self):
        key = "mysecretkey12345"
        ciphertext = None or ""
        with self.assertRaises(AES_logic.EncryptDecryptEmptyMessage):
            decrypt(key, ciphertext)

    def test_decrypt_empty_key_error(self):
        ciphertext = "kHETYJEm1cua9mGD0C3YDZ2YsctWunTX4r4WhA5pBSQ="
        key = None or ""
        with self.assertRaises(AES_logic.EncryptDecryptWithoutKey):
            decrypt(key, ciphertext)

    def teste_decrypt_invalid_key_length(self):
        message = "kHETYJEm1cua9mGD0C3YDZ2YsctWunTX4r4WhA5pBSQ="
        key = "mykey"
        with self.assertRaises(AES_logic.InvalidKeyLength):
            decrypt(key, message)

if __name__ == '__main__':
    unittest.main()
