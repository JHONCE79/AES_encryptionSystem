import psycopg2
import sys
sys.path.append(".")
import config_sample

class Database:
    def __init__(self):
        # Establecer una conexión a la base de datos PostgreSQL utilizando credenciales de config_sample
        self.connection = psycopg2.connect(
            host=config_sample.host,
            database=config_sample.database,
            user=config_sample.user,
            password=config_sample.password,
            sslmode=config_sample.sslmode
        )
        # Crear un objeto cursor para interactuar con la base de datos
        self.cursor = self.connection.cursor()
        # Crear la tabla de mensajes si no existe
        self.create_table()

    def verify_message(self, key, message):
        # Verificar que tanto la clave como el mensaje no estén vacíos
        if not key or not message:
            raise psycopg2.DatabaseError("La clave y el mensaje no pueden estar vacíos.")

    def create_table(self):
        # Consulta SQL para crear la tabla de mensajes si no existe
        create_table_query = """
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            key VARCHAR(255) NOT NULL UNIQUE,
            encrypted_message TEXT NOT NULL
        );
        """
        # Ejecutar la consulta y confirmar los cambios
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def save_message(self, key, message):
        # Verificar la clave y el mensaje antes de guardar
        self.verify_message(key, message)
        try:
            # Insertar la clave y el mensaje en la tabla de mensajes
            self.cursor.execute(
                'INSERT INTO messages ("key", encrypted_message) VALUES (%s, %s)',
                (key, message)
            )
            # Confirmar la transacción
            self.connection.commit()
            return True
        except psycopg2.IntegrityError as e:
            print(f"Error de clave duplicada: {e}")
            self.connection.rollback()
            raise psycopg2.DatabaseError("Ya existe un mensaje con esta clave.")
        except psycopg2.DatabaseError as e:
            print(f"Error al guardar el mensaje: {e}")
            self.connection.rollback()
            return False

    def read_messages(self):
        # Ejecutar una consulta para seleccionar todos los mensajes de la tabla de mensajes
        self.cursor.execute('SELECT id, key, encrypted_message FROM messages;')
        rows = self.cursor.fetchall()
        messages = []
        if rows:
            for row in rows:
                messages.append(f'ID: {row[0]}, Key: {row[1]}, Message: {row[2]}')
        else:
            messages.append("No hay mensajes en la base de datos.")
        return "\n".join(messages)

    def read_message_by_key(self, key):
        # Ejecutar una consulta para seleccionar un mensaje por su clave
        self.cursor.execute('SELECT key, encrypted_message FROM messages WHERE key = %s;', (key,))
        row = self.cursor.fetchone()
        if row:
            return row
        else:
            return "Mensaje no encontrado."

    def update_message(self, id, key, message):
        # Comprobar si el registro existe antes de actualizar
        self.cursor.execute('SELECT * FROM messages WHERE id = %s;', (id,))
        if not self.cursor.fetchone():
            raise psycopg2.DatabaseError("El mensaje con el ID dado no existe.")
        
        try:
            # Actualizar la clave y el mensaje para el ID dado
            self.cursor.execute(
                'UPDATE messages SET "key" = %s, encrypted_message = %s WHERE id = %s',
                (key, message, id)
            )
            # Confirmar la transacción
            self.connection.commit()
            print("Mensaje actualizado exitosamente.")
        except psycopg2.DatabaseError as e:
            print(f"Error al actualizar el mensaje: {e}")
            self.connection.rollback()

    def delete_message(self, id):
        # Comprobar si el registro existe antes de eliminar
        self.cursor.execute('SELECT * FROM messages WHERE id = %s;', (id,))
        if not self.cursor.fetchone():
            raise psycopg2.DatabaseError("El mensaje con el ID dado no existe.")
        
        try:
            # Eliminar el mensaje con el ID dado
            self.cursor.execute('DELETE FROM messages WHERE id = %s;', (id,))
            # Confirmar la transacción
            self.connection.commit()
            print("Mensaje eliminado exitosamente.")
        except psycopg2.DatabaseError as e:
            print(f"Error al eliminar el mensaje: {e}")
            self.connection.rollback()

    def delete_all_messages(self):
        try:
            # Eliminar todos los mensajes de la tabla de mensajes
            self.cursor.execute('DELETE FROM messages;')
            # Confirmar la transacción
            self.connection.commit()
            print("Todos los mensajes eliminados exitosamente.")
        except psycopg2.DatabaseError as e:
            print(f"Error al eliminar mensajes: {e}")
            self.connection.rollback()

    def close(self):
        # Cerrar el cursor y la conexión a la base de datos
        self.cursor.close()
        self.connection.close()