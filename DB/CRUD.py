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
            return True  # Indica que el mensaje se guardó exitosamente
        except Exception as e:
            print(f"Error al guardar el mensaje: {e}")
            self.connection.rollback()
            return False  # Indica que hubo un error

    def read_messages(self):
        self.cursor.execute('SELECT * FROM messages;')
        rows = self.cursor.fetchall()
        if rows:
            for row in rows:
                print(f'ID: {row[0]}, Key: {row[1]}, Message: {row[2]}')
        else:
            print("No hay mensajes disponibles.")

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

    def close(self):
        self.cursor.close()
        self.connection.close()


def main():
    db = Database()
    while True:
        print("\nCRUD Menu:")
        print("1. Create Message")
        print("2. Read Message")
        print("3. Update Message")
        print("4. Delete Message")
        print("5. Exit")

        choice = input(" Choice an option (1-5): ")

        if choice == '1':
            key = input("Enter the key: ")
            message = input("Enter the encrypted message: ")
            db.save_message(key, message)

        elif choice == '2':
            db.read_messages()

        elif choice == '3':
            id = int(input("Enter the ID of the message to update: "))
            key = input("Enter the new key: ")
            message = input("Enter the new encrypted message: ")
            db.update_message(id, key, message)

        elif choice == '4':
            id = int(input("Enter the ID of the message to delete: "))
            db.delete_message(id)

        elif choice == '5':
            print("Exiting...")
            db.close()
            break

        else:
            print("Invalid option, please choose again.")

if __name__ == "__main__":
    main()