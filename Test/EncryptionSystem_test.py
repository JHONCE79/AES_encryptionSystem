import unittest
from src.Logic.AES_logic import AES, encrypt, decrypt


class EncryptionTest(unittest.TestCase):

    #def setUp(self):
    #    self.encryption_strategy = AesEncryption()
    #    self.encryption_context = EncryptionContext(self.encryption_strategy)
    #    self.errors = ErrorsAndExceptions(self.encryption_context)

    #Normal Cases
    def test_encrypt_correctly(self):
        plaintext = "Hello World"
        key = "mysecretkey12345"
        aes = AES(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17')
        ciphertext = "80a60be1771c052070a4c3d4308ccd6604cb4a6c0a5f4f516cec4772337bae2001db749dd363bbc1784f32f42dd90f9f00865475228d44b9deb5850bf43c6c98"
        decrypted_message = AES.decrypt_block(ciphertext)
        self.assertEqual(plaintext, decrypted_message)

    def test_encrypt_short_message(self):
        message = "HelloWorld"
        key = "mysecretkey12345"
        encrypted_message = "j9nteaA4XTc1Jg1aP0N334NxBtiyFi0DrfcZ6HjLNHc="
        decrypted_message = self.encryption_context.decrypt_message(encrypted_message, key)
        self.assertEqual(message, decrypted_message)

    def test_encrypt_message_512_bits(self):
        message = "b" * 512
        key = "mysecretkey12345"
        encrypted_message = "Vn4JgjeUK6Ee4MCIPseJSEGjuMM6mHLAGlYaqdRhYPltCVtqNmusceRzYftJrRyfINX6okmDrvVqgiiqRXJJZJkeQsAy4k0biPBtGrMIx6xWXLJouN2pXPO76sQfNBm0JQ8oC/WjZtFIdP2ms31BXGHoOwnTNrK6z+/Q0J04PdkYMtiR0b6fNCtaoc4MY4shl1GZ94HmVJfPqrCvZSr3w+lQPUjrX0pa2mJs89aLjHjCKARRfUYw83kogV8T0fTYrHHrU9W6IewAeWlXBCcA70KBru5AnbzzOxB91DwfELKeHXf2C6JzbpIYsDlBlCGhG09Hexjtf1j8TF5kjkFP7irsyNhJR2ZaywHrpDOY/x30PGiJ3/8FGngQNJvnC6a+qxXyk8kUtp3QX5eM+DNVWHxgzk9asiEb9F6rIcgvrdCaQ9mK6n+ujvTW39gWlxsGTQpmCWbT1zrWZXA2zy5COJulukxj/dFGnSwL9o8MqwAvphKrTSy6J2CDJ6OECPc1tgJe01KWvZtJPIJtZYvLj7XUvL3k9F3KiRMq1Ncdhu0bor0jwAiXtZzxmJm4qEn/pfnLbZQ5kEYQihmyGyzsn+bDAu5x9cm3SDSk7vUMsyJp/DGtOMEP4J7SdSjHYOm8v2+xFoUjdPWk40lP84AMRxWWfKh3XynI/1bFNU0Nz402sVxBMW45qdLR1mrFkG1HKCOtlArt0ShMUcALy3CYQA=="
        decrypted_message = self.encryption_context.decrypt_message(encrypted_message, key)
        self.assertEqual(message, decrypted_message)

    def test_encrypt_long_message(self):
        message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Curabitur pretium tincidunt lacus. Nulla gravida orci a odio, vitae suscipit ligula vestibulum eu. Fusce vulputate eleifend sapien. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus. Ut libero nisl, dapibus sed, viverra nec, pretium quis, lectus. Suspendisse potenti. Nullam ac urna eu felis dapibus condimentum sit amet a augue."
        key = "mysecretkey12345"
        encrypted_message = "gXuJxoWhkViKE1j/aghzhYvO/ivZHd+bL2DULGIt5Zuz8Ql0KOlR+d0v6Q5DIk25EJqggqX7HqM8rOObWrENJwaCl/Vpj00m3y5YLJScZMOhqaFpjrkSBC/xu4cDz/KIlWIOR2ThZzTCk7gTN14/V1mbs7ElRxNNylGYnJxVfneZYnWIhyTssf0rYUVjdIFB3WW32+RIvvYsBodFFS3RkDOaKi1y7cDYH962lhDDkghFlk1Yy1zkRKhw7FNP/qsfsSYfG07DJPCi+W5yseevI9m9eYaSwor5dSj4/gow01Xnp50v4jfC5JCCPnJiufvIlBC8cdgeGnXFwzVbW9E0JeMSno2YJJH7ItMS3AKlWR21VspcmP+pbRLbz4oyn2ABnYxOJau8V51zlB/zaj1y0yParpn5X31XKc5DeiFUYTdIJiS7y0jcAutQtIGW9Lra8/DJ0wemOeI/k/vi6tUGqr30CNrKVNFYIxCy9LEQEPdI2ZCh1ECs9XxhlUugDq5E7h5IIAQHPuhgYY3TEkwz9/ZUMERXm4omsdWIvdGQileDuh52oiOL5vv6mFI3GN2h27HDMIEYKaWq2SBjFIdE200HPim1RIxSCKvXGAV18l3tjL7mfE8L4whD8ZJW9TNj0+iSrBSp5hzZTVr0XMqmxWwX8lQSBExl/jprsl3C2htwJxO0srrXTVhc58ieWeHFJOyFdgv1wLT6gZH4kiC+j25TW1nDax4ca38FBTt+C208dIeR8jRZTZ6gEvYFSHudjm3eFOM9J6/Er/3uTvZNaZ2v3YPxNmEX2Yg3vAOMfaRtVr78hA7bvPJ7nnQ4fDKDg3Ogbo8QbYGuTm8B+iUh8GMvmjIWVapbZXYrcAzGLdyR5ZSQ2X7uRytF8fWewjjNpGSIRSmZUCBCaB4okUvOp2yQaDw3HOVAEVLtmshquBKNJ0blA0hCJCWjZQ1DRL6UD/HrKeQG29lUq/VcAxJqthQnXms+WUMq0imIWQB+mQ6ENd3NvFpCe+sY3hQyMC+RWKZzJF/6rHRK8CU6/dK3IN3lKzgrAvpsVjv837DKXOvl6jTtRG+JVo8NyFjLfDDd"
        decrypted_message = self.encryption_context.decrypt_message(encrypted_message, key)
        self.assertEqual(message, decrypted_message)

    def test_encrypt_message_special_characters_numbers(self):
        message = "H%$56"
        key = "mysecretkey12345"
        encrypted_message = "SWPLPYTXH4aE72BuV4vgRwhsHDEgcxvOlNogvSqOpEI="
        decrypted_message = self.encryption_context.decrypt_message(encrypted_message, key)
        self.assertEqual(message, decrypted_message)


    def test_encrypt_empty_message_error(self):
        error_handler = ErrorsAndExceptions(self.encryption_context)

        with self.assertRaises(ValueError):
            error_handler.encrypt_empty_message()

    def test_encrypt_list_error(self):
        error_handler = ErrorsAndExceptions(self.encryption_context)

        with self.assertRaises(TypeError):
            error_handler.encrypt_list()

    def test_encrypt_integer_error(self):
        error_handler = ErrorsAndExceptions(self.encryption_context)

        with self.assertRaises(ValueError):
            error_handler.encrypt_integer()

    def test_encrypt_without_key(self):
        error_handler = ErrorsAndExceptions(self.encryption_context)

        with self.assertRaises(KeyError):
            error_handler.encrypt_without_key()


if __name__ == '__main__':
    unittest.main()