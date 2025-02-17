import socket
import threading

HOST = "127.0.0.1"
PORT = 65432

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print("\nMessage reçu :", message.decode())
        except:
            break

threading.Thread(target=receive_messages, daemon=True).start()

while True:
    msg = input("Votre message : ")
    client_socket.sendall(msg.encode())
