import sys
sys.path.append("src")

from EncryptionSystem.AES_logic import encrypt, decrypt

class Console:

    def __init__(self):
        self.aes_instance = None

    @staticmethod
    def show_welcome():
        print()
        print("================================")
        print("BIENVENIDO AL SISTEMA DE ENCRIPTACIÓN")
        print("================================")
        print()

    @staticmethod
    def display_menu():
        print("Menú del Sistema de Encriptación")
        print("1. Encriptar un mensaje")
        print("2. Desencriptar un mensaje")
        print("3. Salir")
        print()

    def get_user_choice(self):
        return input("Selecciona una opción (1-3): ")

    def get_master_key(self):
        return input("Ingresa la clave de encriptación: (debe tener exactamente 16, 24 o 32 caracteres): ")

    def get_message(self):
        return input("Ingresa el mensaje: ")

    def encrypt_message(self):
        key = self.get_master_key()
        message = self.get_message()
        encrypted = encrypt(key, message)
        print("Mensaje Encriptado:", encrypted.hex())

    def decrypt_message(self):
        key = self.get_master_key()
        encrypted_hex = input("Ingresa el mensaje encriptado (en hexadecimal): ")
        encrypted_bytes = bytes.fromhex(encrypted_hex)
        decrypted = decrypt(key, encrypted_bytes)
        print("Mensaje Desencriptado: ", decrypted.decode("utf-8"))

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
                print("Saliendo del Sistema de Encriptación. ¡Adiós!")
                break
            else:
                print("Opción inválida. Por favor selecciona una opción válida. \n")

if __name__ == "__main__":
    console = Console()
    console.run()