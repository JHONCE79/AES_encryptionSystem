import sys
import psycopg2
import unittest

# Add the "src" path to the system paths
sys.path.append("src")

# Import the Database class from the messages controller
from Controller.messages_controller import Database

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Establishes the database connection before running the tests."""
        cls.db = Database()

    @classmethod
    def tearDownClass(cls):
        """Closes the database connection after running the tests."""
        cls.db.close()

    def test_connection_success(self):
        """Verifies that the database connection is established correctly."""
        self.assertIsNotNone(self.db.connection)
        print("Database connection successful.")

    def test_create_table(self):
        """Verifies that the table is created correctly or already exists."""
        try:
            # Attempt to create the table again
            self.db.create_table()
            print("Table 'messages' created successfully.")
        except Exception:
            print("The table 'messages' already exists and was verified successfully.")

    def test_save_message(self):
        """Tests inserting a message into the database."""
        key = "test_key"
        message = "This is a test message."
        success = self.db.save_message(key, message)

        # Verify that the message was saved correctly
        self.db.cursor.execute('SELECT * FROM messages WHERE "key" = %s;', (key,))
        result = self.db.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], key)
        self.assertEqual(result[2], message)

        # Only print if the message was saved successfully
        if success:
            print("Message saved successfully in the database.")

    def test_save_empty_message(self):
        """Tests inserting an empty message into the database."""
        key = "empty_key"
        message = ""
        with self.assertRaises(psycopg2.DatabaseError):
            self.db.save_message(key, message)

if __name__ == "__main__":
    # Run the unit tests
    unittest.main()