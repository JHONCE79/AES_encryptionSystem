#import sys
#sys.path.append("src")
#Logic.AES_logic import decrypt, encrypt

from src.Logic.AES_logic import encrypt, decrypt

class Console:

    def __init__(self):
        self.aes_instance = None

    @staticmethod
    def show_welcome():
        print()
        print("================================")
        print("WELCOME TO THE ENCRYPTION SYSTEM")
        print("================================")
        print()


    @staticmethod
    def display_menu():
        print("Encryption System Menu")
        print("1. Encrypt a message")
        print("2. Decrypt a message")
        print("3. Exit")
        print()

    def get_user_choice(self):
        return input("Select an option (1-3): ")

    def get_master_key(self):
        return input("Enter the encryption key: (must have exactly 16, 24 or 32 characters): ")

    def get_message(self):
        return input("Enter the message: ")

    def encrypt_message(self):
        key = self.get_master_key()
        message = self.get_message()
        encrypted = encrypt(key, message)
        print("Encrypted Message:", encrypted.hex())

    def decrypt_message(self):
        key = self.get_master_key()
        encrypted_hex = input("Enter the encrypted message (in hexadecimal): ")
        encrypted_bytes = bytes.fromhex(encrypted_hex)
        decrypted = decrypt(key, encrypted_bytes)
        print("Decrypted Message: ", decrypted.decode("utf-8"))

    def run(self):
        while True:
            self.show_welcome()
            self.display_menu()
            choice = self.get_user_choice()

            if choice == "1":
                self.encrypt_message()
            elif choice == "2":
                self.decrypt_message()
            elif choice == "3":
                print("Exiting the Encryption System. Goodbye!")
                break
            else:
                print("Invalid choice. Please select a valid option. \n")

if __name__ == "__main__":
    console = Console()
    console.run()
