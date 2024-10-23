import psycopg2
import sys
sys.path.append(".")
import config

class Database:
    def __init__(self):
        # Establish a connection to the PostgreSQL database using credentials from secret_config
        self.connection = psycopg2.connect(
            host = config.host,
            database = config.database,
            user = config.user,
            password = config.password,
            sslmode = config.sslmode
        )
        # Create a cursor object to interact with the database
        self.cursor = self.connection.cursor()
        # Create the messages table if it does not exist
        self.create_table()

    def verify_message(self, key, message):
        # Verify that both key and message are not empty
        if not key or not message:
            raise psycopg2.DatabaseError("The key and message cannot be empty.")

    def create_table(self):
        # SQL query to create the messages table if it does not exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            key VARCHAR(255) NOT NULL,
            encrypted_message TEXT NOT NULL
        );
        """
        # Execute the query and commit the changes
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def save_message(self, key, message):
        # Verify the key and message before saving
        self.verify_message(key, message)
        try:
            # Insert the key and message into the messages table
            self.cursor.execute(
                'INSERT INTO messages ("key", encrypted_message) VALUES (%s, %s)',
                (key, message)
            )
            # Commit the transaction
            self.connection.commit()
            return True
        except psycopg2.DatabaseError as e:
            # Print the error and rollback the transaction in case of failure
            print(f"Error saving message: {e}")
            self.connection.rollback()
            return False

    def read_messages(self):
        # Execute a query to select all messages from the messages table
        self.cursor.execute('SELECT id, key, encrypted_message FROM messages;')
        rows = self.cursor.fetchall()
        messages = []
        if rows:
            # Format each row into a readable string
            for row in rows:
                messages.append(f'ID: {row[0]}, Key: {row[1]}, Message: {row[2]}')
        else:
            messages.append("There are no messages in the database.")
        return "\n".join(messages)
    
    def read_message_by_key(self, key):
        # Execute a query to select a message from the messages table by its id
        self.cursor.execute('SELECT key, encrypted_message FROM messages WHERE key = %s;', (key,))
        row = self.cursor.fetchone()
        if row:
            # Format the row into a readable string
            return row
        else:
            return "Message not found."

    def update_message(self, id, key, message):
        try:
            # Update the key and message for the given id
            self.cursor.execute(
                'UPDATE messages SET "key" = %s, encrypted_message = %s WHERE id = %s',
                (key, message, id)
            )
            # Commit the transaction
            self.connection.commit()
            print("Message updated successfully.")
        except psycopg2.DatabaseError as e:
            # Print the error and rollback the transaction in case of failure
            print(f"Error updating message: {e}")
            self.connection.rollback()

    def delete_message(self, id):
        try:
            # Delete the message with the given id
            self.cursor.execute('DELETE FROM messages WHERE id = %s;', (id,))
            # Commit the transaction
            self.connection.commit()
            print("Message deleted successfully.")
        except psycopg2.DatabaseError as e:
            # Print the error and rollback the transaction in case of failure
            print(f"Error deleting message: {e}")
            self.connection.rollback()

    def delete_all_messages(self):
        try:
            # Delete all messages from the messages table
            self.cursor.execute('DELETE FROM messages;')
            # Commit the transaction
            self.connection.commit()
            print("All messages deleted successfully.")
        except psycopg2.DatabaseError as e:
            # Print the error and rollback the transaction in case of failure
            print(f"Error deleting messages: {e}")
            self.connection.rollback()

    def close(self):
        # Close the cursor and the database connection
        self.cursor.close()
        self.connection.close()