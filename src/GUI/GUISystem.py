from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle

#import sys
#sys.path.append("src")
#Logic.AES_logic import decrypt, encrypt

from src.Logic.AES_logic import decrypt, encrypt


class CustomGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(CustomGridLayout, self).__init__(**kwargs)
        # Usar Canvas para dibujar el fondo
        with self.canvas.before:
            Color(0.231, 0.118, 0.251)  # Color azul (R, G, B, A)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Actualizar el tamaño y la posición del fondo cuando cambien los del layout
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        contenedor = CustomGridLayout(cols=1, padding=10, spacing=10)

        contenedor.add_widget(Label(text="WELCOME TO THE ENCRYPTION SYSTEM", font_size=35))
        contenedor.add_widget(Label(text="Do you want to encrypt or decrypt?", font_size=25))

        encrypt_button = Button(text="Encrypt a message", background_color=(0.929, 0.741, 0.961))
        contenedor.add_widget(encrypt_button)
        encrypt_button.bind(on_press=self.go_to_encrypt)

        decrypt_button = Button(text="Decrypt a message", background_color=(0.929, 0.741, 0.961))
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
        contenedor = CustomGridLayout(cols=1, padding=10, spacing=10)

        contenedor.add_widget(Label(text="Enter the encryption key (must have exactly 16, 24 or 32 characters): "))
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
            self.manager.get_screen('error').set_error_message(f"Error: {str(e)}")
            self.manager.current = 'error'

    def go_back(self, instance):
        self.clear_fields()
        self.manager.current = 'menu'

    def clear_fields(self):
        self.password.text = ""
        self.message.text = ""
        self.encrypted_message.text = ""


class DecryptScreen(Screen):
    def __init__(self, **kwargs):
        super(DecryptScreen, self).__init__(**kwargs)
        contenedor = CustomGridLayout(cols=1, padding=10, spacing=10)

        contenedor.add_widget(Label(text="Enter the encryption key (must have exactly 16, 24 or 32 characters): "))
        self.password = TextInput(password=True)
        contenedor.add_widget(self.password)

        contenedor.add_widget(Label(text="Enter the message to decrypt (in hexadecimal): "))
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
        self.clear_fields()
        self.manager.current = 'menu'

    def clear_fields(self):
        self.password.text = ""
        self.message.text = ""
        self.encrypted_message.text = ""

    def decrypt(self, instance):
        try:
            key = self.password.text
            encrypted_message = self.message.text

            encrypted_message_bytes = bytes.fromhex(encrypted_message)
            decrypted_message = decrypt(key, encrypted_message_bytes)

            self.encrypted_message.text = decrypted_message.decode()

        except Exception as e:
            self.manager.get_screen('error').set_error_message(f"Error: {str(e)}")
            self.manager.current = 'error'


class ErrorScreen(Screen):
    def __init__(self, **kwargs):
        super(ErrorScreen, self).__init__(**kwargs)
        contenedor = CustomGridLayout(cols=1, padding=10, spacing=10)

        self.error_label = Label(text="Error: ", font_size=20)
        contenedor.add_widget(self.error_label)

        back_button = Button(text="Back to Menu")
        contenedor.add_widget(back_button)
        back_button.bind(on_press=self.go_back)

        self.add_widget(contenedor)

    def set_error_message(self, message):
        self.error_label.text = message

    def go_back(self, instance):
        self.manager.get_screen('encrypt').clear_fields()
        self.manager.get_screen('decrypt').clear_fields()
        self.manager.current = 'menu'


class AESapp(App):
    def build(self):
        contenedor = ScreenManager()
        contenedor.add_widget(MenuScreen(name='menu'))
        contenedor.add_widget(EncryptScreen(name='encrypt'))
        contenedor.add_widget(DecryptScreen(name='decrypt'))
        contenedor.add_widget(ErrorScreen(name='error'))
        return contenedor

if __name__ == '__main__':
    AESapp().run()