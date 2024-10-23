import sys
sys.path.append('src')
from Controller import messages_controller

def main():
    db = messages_controller.Database()
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