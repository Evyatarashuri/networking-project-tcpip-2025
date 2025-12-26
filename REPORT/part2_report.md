# Report - Part 2: TCP Chat Application

## 1. Introduction
This section demonstrates a multi-client chat system using TCP sockets.
The server accepts concurrent users through a thread-per-client architecture, allowing real-time messaging.

## 2. System Architecture

**Server Responsibilities:**

- Accept multiple clients.
- Maintain a dictionary of active users.
- Route messages: `sender → server → target`.
- Notify disconnections.

**Client Responsibilities:**

- Connect to the server.
- Send user messages.
- Receive and display messages from the server.

## 3. Concurrency Model

The server uses:

```python
thread = threading.Thread(target=handle_client, args=(conn, addr))
thread.start()
```

Each client gets its own thread → enabling simultaneous communication.
This satisfies the requirement:
"The server must support at least 5 clients concurrently."

## 4. Example Session Screenshots

### 4.1 Server Output

```python
[SERVER STARTED] Listening on port 8080...
[NEW CONNECTION] ('127.0.0.1', 51931)
[NEW CONNECTION] ('127.0.0.1', 51935)
[DISCONNECTED] User3
```

Screenshot:

![Server Running](../part2_chat_application/screenshots/server_running.png)


### 4.2 Multiple Clients Connected

Each client sends messages and receives routed responses.

Screenshot:
![Multiple Clients Connected](../part2_chat_application/screenshots/multiple_clients_connected.png)

## 5. Wireshark TCP Analysis (Chat Application)

- SYN, SYN/ACK, ACK handshake
- PSH/ACK packets containing chat messages
- Multiple simultaneous TCP connections (different source ports)

Screenshot:
![Wireshark Capture](../part2_chat_application/screenshots/wireshark_capture_chat.png)


## 6. Summary
This part demonstrates:

- Multiplexing of multiple TCP connections
- Thread-based concurrency
- Real packet inspection of live chat traffic
- End-to-end message routing logic

The implementation fulfills all project requirements for multi-client TCP communication.
