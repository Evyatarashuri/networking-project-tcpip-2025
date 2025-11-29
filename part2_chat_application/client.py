import socket
import threading

def listen(sock):
    while True:
        try:
            print(sock.recv(1024).decode())
        except:
            break

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create socket
sock.connect(("127.0.0.1", 8080)) # connect to server at port 8080

username = input("Enter username: ") # get username
sock.send(username.encode()) # send hashed username to server

threading.Thread(target=listen, args=(sock,), daemon=True).start() # start listening thread

while True:
    msg = input()
    sock.send(msg.encode())
