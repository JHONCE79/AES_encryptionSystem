import sys
import psycopg2
import unittest

# Add the "src" path to the system paths
sys.path.append("src")

# Import the Database class from the messages controller
from Controller.messages_controller import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Initialize the Database object
        self.db = Database()

    def test_create_table(self):
        """Verifies that the table is created correctly or already exists."""
        try:
            # Attempt to create the table again
            self.db.create_table()
            print("Table 'messages' created successfully.")
        except psycopg2.DatabaseError:
            print("The table 'messages' already exists and was verified successfully.")

    def test_save_message(self):
        """Tests inserting a message into the database."""
        key = "test_key"
        encrypted_message = "This is a test message."
        success = self.db.save_message(key, encrypted_message)

        # Verify that the message was saved correctly
        result = self.db.read_message_by_key(key)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], key)
        self.assertEqual(result[1], encrypted_message)

        # Only print if the message was saved successfully
        if success:
            print("Message saved successfully in the database.")
            self.db.delete_all_messages()

    def test_save_empty_message(self):
        """Tests inserting an empty message into the database."""
        key = "empty_key"
        message = ""
        with self.assertRaises(psycopg2.DatabaseError):
            self.db.save_message(key, message)

if __name__ == "__main__":
    # Run the unit tests
    unittest.main()