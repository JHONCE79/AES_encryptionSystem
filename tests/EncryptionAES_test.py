import unittest

import sys
sys.path.append("src")


from Logic import AES_logic
from Logic.AES_logic import AES, encrypt, decrypt

class EncryptionAESTest(unittest.TestCase):
    # Normal cases
    def test_encrypt_correctly(self):
        message = "Hello World"
        key = "mysecretkey12345"
        encrypted_message = encrypt(key, message)
        decrypted_message = decrypt(key, encrypted_message)
        self.assertEqual(decrypted_message.decode('utf-8'), message)

    def test_encrypt_decrypt_short_message(self):
        message = "Hello World"
        key = "mysecretkey12345"
        encrypted_message = encrypt(key, message)
        decrypted_message = decrypt(key, encrypted_message)
        self.assertEqual(decrypted_message.decode('utf-8'), message)

    def test_encrypt_message_512_bits(self):
        message = "b" * 512
        key = "mysecretkey12345"
        encrypted_message = encrypt(key, message)
        decrypted_message = decrypt(key, encrypted_message)
        self.assertEqual(decrypted_message.decode('utf-8'), message)

    # Special cases
    def test_encrypt_long_message(self):
        message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Curabitur pretium tincidunt lacus. Nulla gravida orci a odio, vitae suscipit ligula vestibulum eu. Fusce vulputate eleifend sapien. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus. Ut libero nisl, dapibus sed, viverra nec, pretium quis, lectus. Suspendisse potenti. Nullam ac urna eu felis dapibus condimentum sit amet a augue."
        key = "mysecretkey12345"
        encrypted_message = encrypt(key, message)
        decrypted_message = decrypt(key, encrypted_message)
        self.assertEqual(decrypted_message.decode('utf-8'), message)

    def test_encrypt_message_special_characters_numbers(self):
        message = "H%$56"
        key = "mysecretkey12345"
        encrypted_message = encrypt(key, message)
        decrypted_message = decrypt(key, encrypted_message)
        self.assertEqual(decrypted_message.decode('utf-8'), message)

    def test_message_space(self):
        message = "  "
        key = "mysecretkey12345"
        encrypted_message = encrypt(key, message)
        decrypted_message = decrypt(key, encrypted_message)
        self.assertEqual(decrypted_message.decode('utf-8'), message)

    #Key cases
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

    #Error cases
    def test_encrypt_empty_key_error(self):
        message = "Hello World"
        key = "" or None
        with self.assertRaises(AES_logic.EncryptDecryptWithoutKey):
            encrypt(key, message)

    def test_encrypt_empty_message_error(self):
        message = "" or None
        key = "mysecretkey12345"
        with self.assertRaises(AES_logic.EncryptDecryptEmptyMessage):
            encrypt(key, message)

    def teste_invalid_key_length(self):
        message = "Hello World"
        key = "mykey"
        with self.assertRaises(AES_logic.InvalidKeyLength):
            encrypt(key, message)

    def test_encrypt_unsupported_message_error(self):
        message = "😀😃"
        key = "mysecretkey12345"
        with self.assertRaises(AES_logic.UnsupportedMessageType):
            encrypt(key, message)


if __name__ == '__main__':
    unittest.main()
