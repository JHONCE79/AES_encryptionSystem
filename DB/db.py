import psycopg2

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            host="ep-delicate-violet-a52i7h4n.us-east-2.aws.neon.tech",
            database="neondb",
            user="neondb_owner",
            password="20CfjJKWmMVb",
            sslmode="require"
        )
        self.cursor = self.connection.cursor()
        self.create_table()  # Asegúrate de que esto se llama

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
            print("Mensaje guardado exitosamente en la base de datos.")
        except Exception as e:
            print(f"Error al guardar el mensaje: {e}")
            self.connection.rollback()

    def close(self):
        self.cursor.close()
        self.connection.close()

if __name__ == "__main__":
    db = Database()
    print("Base de datos y tabla 'messages' creadas correctamente.")
    db.close()