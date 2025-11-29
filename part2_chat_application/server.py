import socket
import threading

clients = {}  # {username: socket}

def handle_client(conn, addr):
    """
    Handle a single client connection.
    Each client gets its own thread and socket.
    """
    print(f"[NEW CONNECTION] {addr}")

    # receive username
    username = conn.recv(1024).decode()
    # store client socket and username in global dict
    clients[username] = conn

    conn.send(f"Welcome {username}! You can now chat.\n".encode())

    # listen for messages from this client
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
    # remove specific client from global dict
    del clients[username]
    # close connection of this client
    conn.close()


def start_server():
    """
    Main socket of the server to accept incoming connections.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 8080))
    server.listen() # TCP Passive open

    print("[SERVER STARTED] Listening on port 8080...")

    # accept clients in a loop
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


# Run the server
if __name__ == "__main__":
    start_server()
