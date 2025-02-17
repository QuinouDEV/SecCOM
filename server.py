import socket
import threading

HOST = "127.0.0.1"
PORT = 65432

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Serveur en écoute sur {HOST}:{PORT}...")

clients = []

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(client_socket, addr):
    print(f"Nouvelle connexion : {addr}")
    clients.append(client_socket)

    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Message reçu de {addr} : {message.decode()}")
            broadcast(message, client_socket)
        except:
            break

    print(f"Connexion fermée : {addr}")
    clients.remove(client_socket)
    client_socket.close()

while True:
    client_socket, addr = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()
