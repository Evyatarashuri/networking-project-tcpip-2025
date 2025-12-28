import socket
import threading

clients = {}  # global dictionary: {username: client_socket}
clients_lock = threading.Lock()  # protect shared dict from race conditions (multiple threads)

def handle_client(conn, addr):
    """
    Handle a single client connection.
    Each client gets its own thread and socket.
    """
    print(f"[NEW CONNECTION] {addr}")

    username = None  # track the connected username for cleanup in finally

    try:
        raw = conn.recv(1024)  # receive up to 1024 bytes from client (blocking call)
        if not raw:
            conn.close()  # client disconnected immediately (EOF)
            return

        username = raw.decode(errors="replace").strip()  # decode bytes -> str; strip whitespace/newlines
        if not username:
            conn.send(b"Invalid username. Connection closing.\n")  # edge case: empty/whitespace username
            conn.close()
            return
        
        if ":" in username:
            conn.send(b"Invalid username. Usernames cannot contain colons.\n")  # prevents parsing ambiguity
            conn.close()
            return
        
        with clients_lock:
            if username in clients:
                conn.send(b"Username already taken. Connection closing.\n")  # edge case: duplicate username
                conn.close()
                return
            clients[username] = conn  # register user only after validation

        conn.send(f"Welcome {username}! You can now chat.\n".encode())  # send greeting (str -> bytes)

        while True:
            try:
                data = conn.recv(1024)  # receive message payload bytes
                if not data:
                    break  # client closed connection gracefully (EOF)

                text = data.decode(errors="replace").strip()  # decode and remove trailing newline/spaces
                if not text:
                    continue  # ignore empty messages (edge case)

                if ":" not in text:
                    conn.send(b"Invalid format. Use: username: message\n")  # edge case: missing delimiter
                    continue

                target, msg = text.split(":", 1)  # split only once so message may contain ':' later
                target = target.strip()  # remove spaces around target username
                msg = msg.lstrip()  # keep trailing spaces; remove only leading spaces after ':'

                if not target:
                    conn.send(b"Invalid target. Use: username: message\n")  # edge case: ": hello"
                    continue

                if target == username:
                    conn.send(b"You cannot send messages to yourself.\n")  # edge case: self-message
                    continue

                with clients_lock:
                    target_conn = clients.get(target)  # safe lookup of target socket
                
                if target_conn:
                    try:
                        target_conn.send(f"[{username}] {msg}\n".encode())  # forward message to target
                    except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, OSError):
                        # edge case: target socket is dead/disconnected while sending
                        with clients_lock:
                            clients.pop(target, None)  # remove stale entry
                        conn.send(b"Target user disconnected.\n")
                else:
                    conn.send(b"User not found.\n")  # edge case: target username not connected

            except (ConnectionResetError, ConnectionAbortedError, OSError):
                break  # edge case: client connection dropped unexpectedly
            except Exception as e:
                print(f"[ERROR] Unexpected error for {addr}: {e}")  # log unexpected failures
                break

    finally:
        if username:
            with clients_lock:
                clients.pop(username, None)  # always remove user from dict on exit
            print(f"[DISCONNECTED] {username}")

        try:
            conn.close()  # ensure socket is closed even on errors
        except OSError:
            pass  # edge case: socket already closed/invalid

def start_server():
    """
    Main socket of the server to accept incoming connections.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP/IPv4 socket
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # allow quick restart after close
    server.bind(("0.0.0.0", 8080))  # listen on all interfaces, port 8080
    server.listen()  # start listening (TCP passive open)

    print("[SERVER STARTED] Listening on port 8080...")

    while True:
        try:
            conn, addr = server.accept()  # blocking: wait for a new client connection
        except KeyboardInterrupt:
            print("\n[SHUTTING DOWN] Server is shutting down.")  # graceful stop on Ctrl+C
            break

        # one thread per client (simple concurrency model)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

    try:
        server.close()  # close the listening socket on shutdown
    except OSError:
        pass  # edge case: socket already closed/invalid


if __name__ == "__main__":
    start_server()  # entry point
