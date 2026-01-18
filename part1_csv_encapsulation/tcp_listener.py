import socket

HOST = "127.0.0.1"
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Listening on 127.0.0.1:8080")

conn, addr = server.accept()
print("Connection from:", addr)

while True:
    data = conn.recv(1024)
    if not data:
        break
    print("Received:", data.decode())

conn.close()
server.close()
