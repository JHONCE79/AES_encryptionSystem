import psycopg2
import sys
sys.path.append(".")
import secret_config

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            host = secret_config.host,
            database = secret_config.database,
            user = secret_config.user,
            password = secret_config.password,
            sslmode = secret_config.sslmode
        )
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            "key" VARCHAR(255) NOT NULL,
            encrypted_message TEXT NOT NULL
        );
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def save_message(self, key, message):
        try:
            self.cursor.execute(
                'INSERT INTO messages ("key", encrypted_message) VALUES (%s, %s)',
                (key, message)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error al guardar el mensaje: {e}")
            self.connection.rollback()
            return False

    def read_messages(self):
        self.cursor.execute('SELECT * FROM messages;')
        rows = self.cursor.fetchall()
        messages = []
        if rows:
            for row in rows:
                messages.append(f'ID: {row[0]}, Key: {row[1]}, Message: {row[2]}')
        else:
            messages.append("No hay mensajes disponibles.")
        return "\n".join(messages)

    def update_message(self, id, key, message):
        try:
            self.cursor.execute(
                'UPDATE messages SET "key" = %s, encrypted_message = %s WHERE id = %s',
                (key, message, id)
            )
            self.connection.commit()
            print("Mensaje actualizado exitosamente.")
        except Exception as e:
            print(f"Error al actualizar el mensaje: {e}")
            self.connection.rollback()

    def delete_message(self, id):
        try:
            self.cursor.execute('DELETE FROM messages WHERE id = %s;', (id,))
            self.connection.commit()
            print("Mensaje eliminado exitosamente.")
        except Exception as e:
            print(f"Error al eliminar el mensaje: {e}")
            self.connection.rollback()

    def delete_all_messages(self):
        try:
            self.cursor.execute('DELETE FROM messages;')
            self.connection.commit()
            print("Todos los mensajes han sido eliminados exitosamente.")
        except Exception as e:
            print(f"Error al eliminar todos los mensajes: {e}")
            self.connection.rollback()

    def close(self):
        self.cursor.close()
        self.connection.close()