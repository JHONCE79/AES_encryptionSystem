from src.Logic.AES_logic import encrypt, decrypt


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        contenedor = GridLayout(cols=1, padding=10, spacing=10)

        contenedor.add_widget(Label(text="WELCOME TO THE ENCRYPTION SYSTEM", font_size=30))
        contenedor.add_widget(Label(text="Do you want to encrypt or decrypt?"))

        encrypt_button = Button(text="Encrypt a message")
        contenedor.add_widget(encrypt_button)
        encrypt_button.bind(on_press=self.go_to_encrypt)

        decrypt_button = Button(text="Decrypt a message")
        contenedor.add_widget(decrypt_button)
        decrypt_button.bind(on_press=self.go_to_decrypt)

        self.add_widget(contenedor)

    def go_to_encrypt(self, instance):
        print("Cambiando a la pantalla de encriptación")
        self.manager.current = 'encrypt'

    def go_to_decrypt(self, instance):
        self.manager.current = 'decrypt'



class EncryptScreen(Screen):
    def __init__(self, **kwargs):
        super(EncryptScreen, self).__init__(**kwargs)
        contenedor = GridLayout(cols=1, padding=10, spacing=10)

        contenedor.add_widget(Label(text="Enter the encryption key: "))
        self.password = TextInput(password=True)
        contenedor.add_widget(self.password)

        contenedor.add_widget(Label(text="Enter the message: "))
        self.message = TextInput()
        contenedor.add_widget(self.message)

        self.encrypted_message = TextInput()
        contenedor.add_widget(self.encrypted_message)

        encrypt_button = Button(text="Encrypt")
        contenedor.add_widget(encrypt_button)
        encrypt_button.bind(on_press=self.encrypt)

        back_button_go_back = Button(text="Back")
        contenedor.add_widget(back_button_go_back)
        back_button_go_back.bind(on_press=self.go_back)


        self.add_widget(contenedor)

    def encrypt(self, instance):
        try:
            key = self.password.text
            message = self.message.text

            encrypted_message = encrypt(key, message)
            encrypted_message_hex = encrypted_message.hex()

            self.encrypted_message.text = encrypted_message_hex

        except Exception as e:
            # En caso de error, muestra un mensaje en el label
            #CAMBIAR LOS CASOS DE ERROS PARA LOS UWE SE VAN A CREAR
            self.encrypted_message.text = f"Error: {str(e)}"


    def go_back(self, instance):
        self.manager.current = 'menu'


class DecryptScreen(Screen):
    def __init__(self, **kwargs):
        super(DecryptScreen, self).__init__(**kwargs)
        contenedor = GridLayout(cols=1, padding=10, spacing=10)

        contenedor.add_widget(Label(text="Enter the encryption key: "))
        self.password = TextInput(password=True)
        contenedor.add_widget(self.password)

        contenedor.add_widget(Label(text="Enter the message to decrypt(in hexadecimal): "))
        self.message = TextInput()
        contenedor.add_widget(self.message)

        self.encrypted_message = TextInput()
        contenedor.add_widget(self.encrypted_message)

        decrypt_button = Button(text="Decrypt")
        contenedor.add_widget(decrypt_button)
        decrypt_button.bind(on_press=self.decrypt)

        back_button_go_back = Button(text="Back")
        contenedor.add_widget(back_button_go_back)
        back_button_go_back.bind(on_press=self.go_back)

        self.add_widget(contenedor)

    def go_back(self, instance):
        self.manager.current = 'menu'

    def decrypt(self, instance):
        try:
            key = self.password.text
            encrypted_message = self.message.text

            encrypted_message_bytes = bytes.fromhex(encrypted_message)
            decrypted_message = decrypt(key, encrypted_message_bytes)

            self.encrypted_message.text = decrypted_message.decode()

        except Exception as e:
            # En caso de error, mostrar el mensaje de error en el mismo TextInput
            #CAMBIAR LOS CASOS DE ERROS PARA LOS UWE SE VAN A CREAR
            self.encrypted_message.text = f"Error: {str(e)}"


class AESapp(App):
    def build(self):
        contenedor = ScreenManager()
        contenedor.add_widget(MenuScreen(name='menu'))
        contenedor.add_widget(EncryptScreen(name='encrypt'))
        contenedor.add_widget(DecryptScreen(name='decrypt'))
        return contenedor

if __name__ == '__main__':
    AESapp().run()
