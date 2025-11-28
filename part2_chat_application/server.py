import socket
import threading

clients = {}  # {username: socket}

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr}")

    # receive username
    username = conn.recv(1024).decode()
    clients[username] = conn

    conn.send(f"Welcome {username}! You can now chat.\n".encode())

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            # data format: "target_username: message"
            if ":" not in data:
                conn.send(b"Invalid format. Use: username: message\n")
                continue

            target, msg = data.split(":", 1)

            if target in clients:
                clients[target].send(f"[{username}] {msg}".encode())
            else:
                conn.send(b"User not found.\n")

        except:
            break

    print(f"[DISCONNECTED] {username}")
    del clients[username]
    conn.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8080))
    server.listen()

    print("[SERVER STARTED] Listening on port 8080...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    start_server()
