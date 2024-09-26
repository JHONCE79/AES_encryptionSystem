from src.Logic.AES_logic import *
class Console:

    def main(self) -> None:
        print("Menú de AES:")
        print("1. Encriptar mensaje")
        print("2. Desencriptar mensaje")
        print("3. Salir")

        while True:
            opcion = input("Ingrese una opción: ")

            if opcion == "1":
                clave = input("Ingrese la clave de encriptación: ")
                mensaje = input("Ingrese el mensaje a encriptar: ")
                encriptado = encrypt(clave, mensaje)
                print("Mensaje encriptado:", encriptado.hex())
            elif opcion == "2":
                clave = input("Ingrese la clave de desencriptación: ")
                mensaje_encriptado = input("Ingrese el mensaje encriptado (en hexadecimal): ")
                mensaje_encriptado = bytes.fromhex(mensaje_encriptado)
                desencriptado = decrypt(clave, mensaje_encriptado)
                print("Mensaje desencriptado:", desencriptado.decode("utf-8"))
            elif opcion == "3":
                print("Adiós!")
                break
            else:
                print("Opción inválida. Intente de nuevo.")

    if __name__ == "__main__":
        main('self')