import socket
import threading
import rsa
import random
import tkinter as tk
from tkinter import scrolledtext

HOST = "127.0.0.1"
PORT = 65432

pseudo = f"User{random.randint(1000, 9999)}"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

public_key_data = client_socket.recv(1024)
public_key = rsa.PublicKey.load_pkcs1(public_key_data)

sym_key = random.randint(1, 25)
print(f"Clé symétrique générée : {sym_key}")

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

def send_message():
    message = msg_entry.get()
    if message:
        encrypted_msg = caesar_cipher(f"[{pseudo}] {message}", sym_key)
        client_socket.sendall(encrypted_msg.encode())
        msg_entry.delete(0, tk.END)
        
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"Moi: {message}\n")
        chat_display.config(state=tk.DISABLED)

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            decrypted_message = caesar_cipher(message.decode(), -sym_key)
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, decrypted_message + "\n")
            chat_display.config(state=tk.DISABLED)
        except:
            break

root = tk.Tk()
root.title("Chat Sécurisé")
root.iconbitmap("chat_secure.ico")


chat_display = scrolledtext.ScrolledText(root, state=tk.DISABLED, width=50, height=20)
chat_display.pack(padx=10, pady=10)

msg_entry = tk.Entry(root, width=40)
msg_entry.pack(pady=5, padx=10, side=tk.LEFT)
msg_entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(root, text="Envoyer", command=send_message)
send_button.pack(pady=5, padx=10, side=tk.RIGHT)

threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()
