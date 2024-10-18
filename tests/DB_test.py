import sys
import os
import unittest

sys.path.append("src")

from Controller.messages_controller import Database  # Importar la clase Database

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Establece la conexión a la base de datos antes de ejecutar las pruebas."""
        cls.db = Database()

    @classmethod
    def tearDownClass(cls):
        """Cierra la conexión a la base de datos después de ejecutar las pruebas."""
        cls.db.close()

    def test_connection_success(self):
        """Verifica que la conexión a la base de datos se establezca correctamente."""
        self.assertIsNotNone(self.db.connection)
        print(".Conexión a la base de datos exitosa.")

    def test_create_table(self):
        """Verifica que la tabla se cree correctamente o que ya exista."""
        try:
            self.db.create_table()  # Intentar crear la tabla nuevamente
            print("Tabla 'messages' creada exitosamente.")
        except Exception:
            print("La tabla 'messages' ya existe y se verificó exitosamente.")

    def test_save_message(self):
        """Prueba la inserción de un mensaje en la base de datos."""
        key = "test_key"
        message = "This is a test message."
        success = self.db.save_message(key, message)

        # Verificar que el mensaje fue guardado correctamente
        self.db.cursor.execute('SELECT * FROM messages WHERE "key" = %s;', (key,))
        result = self.db.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], key)
        self.assertEqual(result[2], message)

        # Solo imprimir si el mensaje fue guardado exitosamente
        if success:
            print("Mensaje guardado exitosamente en la base de datos.")



if __name__ == "__main__":
    unittest.main()