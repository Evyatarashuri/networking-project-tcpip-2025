import socket
import threading

def listen(sock):
    """
    Background thread:
    continuously receives data from the server and prints it.
    """
    while True:
        try:
            data = sock.recv(1024)  # receive up to 1024 bytes from server (blocking)
            if not data:
                print("\n[Disconnected from server]")  # server closed the connection (EOF)
                break
            print(data.decode(errors="replace"), end="")  # decode bytes -> str, server already adds '\n'
        except OSError:
            break

# create a TCP/IPv4 socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server (loopback interface, port 8080)
sock.connect(("127.0.0.1", 8080))

# get username from user
username = input("Enter username: ").strip()

# basic client-side validation to match server rules
if not username or ":" in username:
    print("Invalid username (cannot be empty or contain ':').")
    sock.close()
    raise SystemExit

# send username to server (newline helps message framing)
sock.send((username + "\n").encode())

# start background thread to listen for incoming messages
threading.Thread(
    target=listen,
    args=(sock,),
    daemon=True  # daemon thread exits automatically when main thread exits
).start()

# main loop: read user input and send messages to server
while True:
    try:
        msg = input()  # user types: target: message
        sock.send((msg + "\n").encode())  # send message as bytes with delimiter
    except (EOFError, KeyboardInterrupt):
        break  # user requested exit (Ctrl+D / Ctrl+C)
    except OSError:
        break  # connection lost

# close socket on exit to release system resources
sock.close()
