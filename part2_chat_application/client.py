import socket
import threading

def listen(sock):
    while True:
        try:
            print(sock.recv(1024).decode())
        except:
            break

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 8080))

username = input("Enter username: ")
sock.send(username.encode())

threading.Thread(target=listen, args=(sock,), daemon=True).start()

while True:
    msg = input()
    sock.send(msg.encode())
