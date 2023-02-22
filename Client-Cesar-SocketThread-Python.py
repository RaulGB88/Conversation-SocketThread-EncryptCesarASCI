import imp
import socket
import sys
import lib.socketLibrary
import lib.encryptCesarASCI

from Crypto.Cipher import AES
from setuptools import sic

HOST = '127.0.0.1'
PORT = 5008

BYE = 'bye'
MESSAGE_TO_KEY = "Puedes mandarme la clave?"
MESSAGE_TO_INPUT = "Indica tu mensaje: "


def client_program():
    """ Ejecuta el programa Cliente """

    try:
        # 1- Creamos el Socket.
        socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket cliente creado')
    except socket.error:
        print('Fallo en la creación del socket cliente')
        sys.exit()

    # 2- Conectamos el Socket cliente al servidor
    socket_client.connect((HOST, PORT))

    execute(socket_client)


def execute(socket_client):
    """ Ejecuta la logica del programa """

    with socket_client:

        print(f'Conexión exitosa con el servidor.')

        # Recieve message with Key from Server
        key_encrypted = socket_client.recv(1024)
        # Decode a key
        key_decrypted = key_encrypted.decode()
        # Format a key to text value
        key = str(key_decrypted).lower()

        # Encrypte a message
        encrypted_message = lib.encryptCesarASCI.encrypt("Thank you for a key", key)
        # Send the encrypted message with a key and recieve an encrypted message of Client
        recieve_encrypted_message = lib.socketLibrary.messagesText(socket_client, encrypted_message)
        # Decrypte a message of Client with a key
        recieve_decrypted_message = lib.encryptCesarASCI.decrypt(recieve_encrypted_message, key)

        while recieve_decrypted_message != BYE:
        
            # Decrypte the message of Server with a key
            recieve_decrypted_message = lib.encryptCesarASCI.decrypt(recieve_encrypted_message, key)
            # Print a decrypted message of Server
            print(recieve_decrypted_message)

            # Input the message
            input_message = input(MESSAGE_TO_INPUT)
            # Encrypte the input messsage
            encrypted_message = lib.encryptCesarASCI.encrypt(input_message, key)
            # Send the encrypted message with a key and recieve an encrypted message of Server
            recieve_encrypted_message = lib.socketLibrary.messagesText(socket_client, encrypted_message)
            # Decrypte a message of Client with a key
            recieve_decrypted_message = lib.encryptCesarASCI.decrypt(recieve_encrypted_message, key)


if __name__ == '__main__':
    client_program()
