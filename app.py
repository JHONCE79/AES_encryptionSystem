from flask import Flask, render_template, request, flash
from src.EncryptionSystem.AES_logic import AES, get_key_iv, EncryptDecryptWithoutKey, EncryptDecryptEmptyMessage, InvalidKeyLength, UnsupportedMessageType, encrypt, decrypt
import os
import psycopg2
import config_sample

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Configuración de constantes
SALT_SIZE = 16
HMAC_SIZE = 32
WORKLOAD = 100000

class Database:
    def __init__(self):  # Asegúrate de usar __init__
        self.connection = psycopg2.connect(
            host=config_sample.host,
            database=config_sample.database,
            user=config_sample.user,
            password=config_sample.password,
            sslmode=config_sample.sslmode
        )
        self.cursor = self.connection.cursor()  # Inicializa el cursor aquí
        self.create_table()

    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            key VARCHAR(255) NOT NULL UNIQUE,
            encrypted_message TEXT NOT NULL
        );
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def save_message(self, key, message):
        if not key or not message:
            raise psycopg2.DatabaseError("La clave y el mensaje no pueden estar vacíos.")
        try:
            self.cursor.execute(
                'INSERT INTO messages (key, encrypted_message) VALUES (%s, %s)',
                (key, message)
            )
            self.connection.commit()
            return True
        except psycopg2.IntegrityError:
            self.connection.rollback()
            raise psycopg2.DatabaseError("Ya existe un mensaje con esta clave.")

    def read_messages(self):
        self.cursor.execute("SELECT id, key, encrypted_message FROM messages")
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()
# Instancia de la clase Database
db = Database()

@app.route('/')
def index():
    return render_template('index.html', encrypted_text=None)

@app.route('/encrypt', methods=['POST'])
def encrypt_text():
    text_to_encrypt = request.form.get('text_to_encrypt')
    user_key = request.form.get('encryption_key')

    if not text_to_encrypt:
        flash('Por favor, ingrese el texto a cifrar')
        return render_template('index.html', encrypted_text=None)

    if not user_key or len(user_key) not in [16, 24, 32]:
        flash('La clave debe tener exactamente 16, 24 o 32 caracteres')
        return render_template('index.html', encrypted_text=None)

    try:
        encrypted_text = encrypt(user_key.encode('utf-8'), text_to_encrypt, workload=WORKLOAD)
        encrypted_hex = encrypted_text.hex()
        
        # Guardar el mensaje cifrado en la base de datos
        db.save_message(user_key, encrypted_hex)

        flash('Texto cifrado exitosamente. Use el siguiente código en el campo de descifrado para recuperarlo.')
        return render_template('index.html', encrypted_text=encrypted_hex)
    except (EncryptDecryptWithoutKey, EncryptDecryptEmptyMessage, InvalidKeyLength, UnsupportedMessageType) as e:
        flash(str(e))
    
    return render_template('index.html', encrypted_text=None)

@app.route('/decrypt', methods=['POST'])
def decrypt_text():
    text_to_decrypt = request.form.get('text_to_decrypt')
    user_key = request.form.get('encryption_key')

    if not text_to_decrypt:
        flash('Por favor, ingrese el texto a descifrar')
        return render_template('index.html', encrypted_text=None)

    if not user_key or len(user_key) not in [16, 24, 32]:
        flash('La clave debe tener exactamente 16, 24 o 32 caracteres')
        return render_template('index.html', encrypted_text=None)

    try:
        encrypted_data = bytes.fromhex(text_to_decrypt)
        
        decrypted_text = decrypt(user_key.encode('utf-8'), encrypted_data, workload=WORKLOAD).decode('utf-8')
        flash(f'Texto descifrado: {decrypted_text}')
    except (EncryptDecryptWithoutKey, EncryptDecryptEmptyMessage, InvalidKeyLength, UnsupportedMessageType) as e:
        flash(str(e))
    except ValueError as e:
        flash(f"Error al descifrar: {e}")
    
    return render_template('index.html', encrypted_text=None)

@app.route('/messages', methods=['GET'])
def show_messages():
    # Obtener todos los mensajes guardados en la base de datos
    messages = db.read_messages()
    return render_template('messages.html', messages=messages)

@app.route('/view-database', methods=['GET'])
def view_database():
    # Obtener todos los registros guardados en la base de datos
    records = db.read_messages()
    return render_template('view_database.html', records=records)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

# Cerrar la conexión a la base de datos al finalizar la aplicación
@app.teardown_appcontext
def close_db(exception):
    db.close()