import sys
sys.path.append('src')
from Controller import messages_controller

def main():
    db = messages_controller.Database()
    while True:
        print("\nMenú CRUD:")
        print("1. Crear Mensaje")
        print("2. Leer Mensaje")
        print("3. Actualizar Mensaje")
        print("4. Eliminar Mensaje")
        print("5. Salir")

        choice = input("Selecciona una opción (1-5): ")

        if choice == '1':
            key = input("Ingresa la clave: ")
            message = input("Ingresa el mensaje encriptado: ")
            db.save_message(key, message)

        elif choice == '2':
            print(db.read_messages())  

        elif choice == '3':
            id = int(input("Ingresa el ID del mensaje a actualizar: "))
            key = input("Ingresa la nueva clave: ")
            message = input("Ingresa el nuevo mensaje encriptado: ")
            db.update_message(id, key, message)

        elif choice == '4':
            id = int(input("Ingresa el ID del mensaje a eliminar: "))
            db.delete_message(id)

        elif choice == '5':
            print("Saliendo...")
            db.close()
            break

        else:
            print("Opción inválida, por favor elige de nuevo.")

if __name__ == "__main__":
    main()