from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
import sys

sys.path.append("src")

from EncryptionSystem.AES_logic import decrypt, encrypt
from Controller import messages_controller


class CustomGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(CustomGridLayout, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0.231, 0.118, 0.251)
            self.rect = Rectangle(size=self.size, pos=self.pos)
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

        see_messages_button = Button(text="See messages", background_color=(0.929, 0.741, 0.961))
        contenedor.add_widget(see_messages_button)
        see_messages_button.bind(on_press=self.go_to_see_messages)

        self.add_widget(contenedor)

    def go_to_encrypt(self, instance):
        self.manager.current = 'encrypt'

    def go_to_decrypt(self, instance):
        self.manager.current = 'decrypt'

    def go_to_see_messages(self, instance):
        self.manager.current = 'see_messages'


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

            if App.get_running_app().database.save_message(key, encrypted_message_hex):
                self.encrypted_message.text = encrypted_message_hex
                print("Mensaje guardado en la base de datos.")
            else:
                print("No se pudo guardar el mensaje en la base de datos.")

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

        self.decrypted_message = TextInput()
        contenedor.add_widget(self.decrypted_message)

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
        self.decrypted_message.text = ""

    def decrypt(self, instance):
        try:
            key = self.password.text
            encrypted_message = self.message.text

            encrypted_message_bytes = bytes.fromhex(encrypted_message)
            decrypted_message = decrypt(key, encrypted_message_bytes)

            self.decrypted_message.text = decrypted_message.decode()

        except Exception as e:
            self.manager.get_screen('error').set_error_message(f"Error: {str(e)}")
            self.manager.current = 'error'


class SeeMessagesScreen(Screen):
    def __init__(self, **kwargs):
        super(SeeMessagesScreen, self).__init__(**kwargs)
        contenedor = CustomGridLayout(cols=1, padding=10, spacing=10)

        contenedor.add_widget(Label(text="Messages: "))
        self.messages_textbox = TextInput(size_hint=(1, 1), multiline=True, readonly=True)
        contenedor.add_widget(self.messages_textbox)

        update_messages = Button(text="Update messages")
        contenedor.add_widget(update_messages)
        update_messages.bind(on_press=self.update_messages)

        id_label = Label(text="Enter the ID of the message you want to delete: ")
        contenedor.add_widget(id_label)
        self.id_to_delete = TextInput(size_hint=(1, None), height=30)
        contenedor.add_widget(self.id_to_delete)

        delete_message = Button(text="Delete message")
        contenedor.add_widget(delete_message)
        delete_message.bind(on_press=self.delete_message)

        delete_all_messages = Button(text="Delete all messages")
        contenedor.add_widget(delete_all_messages)
        delete_all_messages.bind(on_press=self.delete_all_messages)

        back_button = Button(text="Back to Menu")
        contenedor.add_widget(back_button)
        back_button.bind(on_press=self.go_back)

        self.add_widget(contenedor)

    def go_back(self, instance):
        self.manager.current = 'menu'

    def update_messages(self, instance=None):
        messages = App.get_running_app().database.read_messages()
        if messages is None:
            messages = ""
        self.messages_textbox.text = messages

    def delete_message(self, instance):
        message_id = self.id_to_delete.text
        if message_id:
            try:
                App.get_running_app().database.delete_message(message_id)
                self.update_messages()
                self.id_to_delete.text = ""
            except Exception as e:
                self.manager.get_screen('error').set_error_message(f"Error: {str(e)}")
                self.manager.current = 'error'

    def delete_all_messages(self, instance):
        try:
            App.get_running_app().database.delete_all_messages()
            self.update_messages()
        except Exception as e:
            self.manager.get_screen('error').set_error_message(f"Error: {str(e)}")
            self.manager.current = 'error'

    def on_enter(self):
        self.update_messages()


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
        self.database = messages_controller.Database()
        contenedor = ScreenManager()
        contenedor.add_widget(MenuScreen(name='menu'))
        contenedor.add_widget(EncryptScreen(name='encrypt'))
        contenedor.add_widget(DecryptScreen(name='decrypt'))
        contenedor.add_widget(SeeMessagesScreen(name='see_messages'))
        contenedor.add_widget(ErrorScreen(name='error'))
        return contenedor

if __name__ == '__main__':
    AESapp().run()
