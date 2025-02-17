import socket
import threading
import rsa

HOST = "127.0.0.1"
PORT = 65432

# Générer une paire de clés RSA
(public_key, private_key) = rsa.newkeys(512)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Serveur en écoute sur {HOST}:{PORT}...")

clients = {}
keys = {}

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def broadcast(decrypted_message, sender_socket):
    for client, key in keys.items():
        if client != sender_socket:
            try:
                # Chiffrement du message avec la clé du destinataire
                encrypted_message = caesar_cipher(decrypted_message, key)
                client.sendall(encrypted_message.encode())
            except:
                client.close()
                del clients[client]
                del keys[client]

def handle_client(client_socket, addr):
    print(f"Nouvelle connexion : {addr}")
    
    # Envoi de la clé publique au client
    client_socket.sendall(public_key.save_pkcs1())

    # Réception de la clé symétrique chiffrée
    encrypted_key = client_socket.recv(1024)
    sym_key = int(rsa.decrypt(encrypted_key, private_key).decode())
    keys[client_socket] = sym_key
    clients[addr] = client_socket

    print(f"Clé symétrique reçue de {addr}: {sym_key}")

    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            
            # Déchiffrement du message reçu avec la clé du client
            decrypted_message = caesar_cipher(message.decode(), -sym_key)
            print(f"Message reçu de {addr} : {decrypted_message}")

            # Retransmission aux autres clients avec leurs propres clés symétriques
            broadcast(decrypted_message, client_socket)  
        except:
            break

    print(f"Connexion fermée : {addr}")
    del clients[addr]
    del keys[client_socket]
    client_socket.close()

while True:
    client_socket, addr = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()
