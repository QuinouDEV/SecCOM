import socket
import threading
import rsa
import random

HOST = "127.0.0.1"
PORT = 65432

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Récupérer la clé publique du serveur
public_key_data = client_socket.recv(1024)
public_key = rsa.PublicKey.load_pkcs1(public_key_data)

sym_key = random.randint(1, 25)
print(f"Clé symétrique générée : {sym_key}")

# Chiffrement de la la clé symétrique avec la clé publique du serveur
encrypted_key = rsa.encrypt(str(sym_key).encode(), public_key)
client_socket.sendall(encrypted_key)

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            decrypted_message = caesar_cipher(message.decode(), -sym_key)
            print("\nMessage déchiffré : " + decrypted_message)
        except:
            break

threading.Thread(target=receive_messages, daemon=True).start()

while True:
    msg = input("\nVotre message : ")
    encrypted_msg = caesar_cipher(msg, sym_key)
    client_socket.sendall(encrypted_msg.encode())
