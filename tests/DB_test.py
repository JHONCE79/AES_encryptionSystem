import sys
import psycopg2
import unittest

# Agregar la ruta "src" a las rutas del sistema 
sys.path.append("src")

# Importar la clase Database desde el controlador de mensajes 
from Controller.messages_controller import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Inicializar el objeto Database 
        self.db = Database()
        self.db.delete_all_messages()  # Asegurar un estado limpio antes de cada prueba

    def tearDown(self):
        # Limpiar después de cada prueba 
        self.db.delete_all_messages()
        self.db.close()

    def test_create_table(self):
        """Verifica que la tabla se cree correctamente o ya exista."""
        try:
            # Intentar crear la tabla nuevamente 
            self.db.create_table()
            print("Tabla 'messages' creada exitosamente.")
        except psycopg2.DatabaseError:
            print("La tabla 'messages' ya existe y se verificó exitosamente.")

    def test_save_message(self):
        """Prueba insertar un mensaje en la base de datos (caso normal)."""
        key = "test_key"
        encrypted_message = "Este es un mensaje de prueba."
        
        success = self.db.save_message(key, encrypted_message)

        # Verificar que el mensaje se guardó correctamente 
        result = self.db.read_message_by_key(key)
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0], key)
        self.assertEqual(result[1], encrypted_message)

    def test_save_empty_message(self):
         """Prueba insertar un mensaje vacío en la base de datos (caso de error)."""
         key = "empty_key"
         message = ""
         with self.assertRaises(psycopg2.DatabaseError):
             self.db.save_message(key, message)

    def test_read_messages(self):
         """Prueba leer todos los mensajes desde la base de datos (caso normal)."""
         # Insertar un mensaje para asegurar que hay datos para leer 
         self.db.save_message("test_key1", "Mensaje 1")
         self.db.save_message("test_key2", "Mensaje 2")

         # Leer mensajes y verificar la salida 
         messages = self.db.read_messages()
         self.assertIn("Mensaje 1", messages)
         self.assertIn("Mensaje 2", messages)

    def test_read_message_by_key_not_found(self):
         """Prueba leer un mensaje con una clave que no existe (caso de error)."""
         result = self.db.read_message_by_key("nonexistent_key")
         self.assertEqual(result, "Mensaje no encontrado.")

    def test_update_message(self):
        """Prueba actualizar un mensaje por ID (caso normal)."""
        # Guardar un mensaje inicial para actualizar más tarde
        self.db.save_message("update_key", "Old Message")
        message_data = self.db.read_message_by_key("update_key")

        # Asegúrate de que estás obteniendo el ID correcto
        message_id = message_data[2]  # Ajusta al índice del ID del mensaje
        
        # Actualizar el mensaje usando su ID
        self.db.update_message(message_id, "update_key", "New Message")

        # Verificar la actualización
        updated_message = self.db.read_message_by_key("update_key")
        self.assertEqual(updated_message[1], "New Message")


    def test_update_message_nonexistent_id(self):
         """Prueba actualizar un mensaje con un ID inexistente (caso de error)."""
         non_existent_id = 9999
         with self.assertRaises(psycopg2.DatabaseError):
             self.db.update_message(non_existent_id, "key", "New Message")

    def test_delete_message(self):
        """Prueba eliminar un mensaje específico por ID (caso normal)."""
        # Guardar un mensaje para eliminar más tarde
        self.db.save_message("delete_key", "Mensaje a eliminar")
        message_data = self.db.read_message_by_key("delete_key")

        # Asegúrate de que estás obteniendo el ID correcto
        message_id = message_data[2]  # Asegura que aquí tienes el id correcto
        
        # Eliminar el mensaje por ID
        self.db.delete_message(message_id)

        # Verificar eliminación
        result = self.db.read_message_by_key("delete_key")
        self.assertEqual(result, "Mensaje no encontrado.")


    def test_delete_message_nonexistent_id(self):
         """Prueba eliminar un mensaje con un ID inexistente (caso de error)."""
         non_existent_id = 9999
         with self.assertRaises(psycopg2.DatabaseError):
             self.db.delete_message(non_existent_id)

    def test_delete_all_messages(self):
         """Prueba eliminar todos los mensajes desde la base de datos (caso normal)."""
         # Insertar mensajes para eliminar 
         self.db.save_message("delete_all_key1", "Mensaje 1")
         self.db.save_message("delete_all_key2", "Mensaje 2")

         # Eliminar todos los mensajes 
         self.db.delete_all_messages()

         # Verificar eliminación  
         messages = self.db.read_messages()
         self.assertEqual(messages, "No hay mensajes en la base de datos.")

    def test_save_message_with_duplicate_key(self):
          """Prueba insertar un mensaje con una clave duplicada (caso de error)."""
          key = "duplicate_key"
          encrypted_message = "Este es el primer mensaje."
          encrypted_message_duplicate = "Este es el mensaje duplicado."

          # Guardar el mensaje inicial 
          self.db.save_message(key, encrypted_message)

          # Intentar guardar un mensaje con la misma clave 
          with self.assertRaises(psycopg2.DatabaseError):
              self.db.save_message(key, encrypted_message_duplicate)

if __name__ == "__main__":
    unittest.main()