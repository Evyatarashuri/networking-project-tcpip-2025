# TCP/IP Networking Project 2025

This project demonstrates a complete **TCP/IP networking workflow**, including packet encapsulation, traffic generation, and multi-client communication over TCP.

---

## Part 1 - Encapsulation & Traffic Analysis

**Key Features:**
- Loading application-level messages from CSV  
- Simulating encapsulation through the **TCP/IP stack** (Application → Transport → Network → Link)  
- Sending custom **TCP packets** over the loopback interface  
- Capturing real traffic with **Wireshark**  
- Inspecting headers (TCP, IP) and analyzing packet flow

---

## Part 2 - TCP Chat Application

**Key Features:**
- TCP socket server handling **multiple clients concurrently**
- **Thread-per-client** architecture for parallel message handling
- Direct user-to-user message routing (`sender → server → target`)
- Real-time chat demonstrated with logs and live network traffic captures
- Shows core networking concepts: connections, sockets, threading, and message framing

---

## Included in the Repository

- **Part 1 - CSV, Encapsulation & Wireshark Capture**
- **Part 2 - TCP Chat Application (Server + Multiple Clients)**
- **Full Wireshark `.pcapng` captures**
- **Executed Jupyter Notebook**
- **Screenshots & Explanations**

---

## How to Download:

1. Clone the repository:

   ```bash
   git clone https://github.com/Evyatarashuri/networking-project-tcpip-2025.git
   cd networking-project-tcpip-2025
    ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:

   ```bash
   pip3 install -r requirements.txt
   ```

---

## How to Run:

### Part 1 – Encapsulation & Traffic Analysis

1. Open the Jupyter Notebook:

   ```bash
   jupyter notebook
   ```

2. Navigate to:

   ```
   part1_csv_encapsulation/encapsulation_notebook.ipynb
   ```

3. Run all cells:

- Loads CSV input
- Generates encapsulated TCP messages
- Saves results
- Produces Wireshark-capturable traffic

4. Open the generated `.pcapng` file in Wireshark for analysis.

### Part 2 – TCP Chat Application

**Start the Server**

Run the server:

```bash
python3 part2_chat_application/server.py
```

**Run Multiple Clients**

Each client runs in a separate terminal window:

```bash
python3 part2_chat_application/client.py
```

You will be prompted:
```bash
Enter username:
```

Then users can chat in real-time:

- Messages are routed via the server
- Each client runs on its own thread
- Wireshark captures real TCP traffic

### Optional: Capture Traffic in Wireshark

1. Open Wireshark and start a new capture on the loopback interface (lo0).
2. Use the display filter:
   ```bash
   tcp.port == 8080
   ```
3. Analyze the captured packets for TCP handshake, message framing, and routing.

---

## Project Screenshots

### Part 1 - Encapsulation, CSV & Wireshark

**CSV Input Preview:**
![CSV Input Preview](./part1_csv_encapsulation/screenshots/csv_preview.png)

**Jupyter Notebook:**
![Jupyter Notebook](./part1_csv_encapsulation/screenshots/jupyter_encapsulation_preview.png)

**Wireshark Capture:**
![Wireshark Capture](./part1_csv_encapsulation/screenshots/wireshark_capture_part1.jpeg)

### Part 2 - TCP Chat Application

**Server Running:**
![Server Running](./part2_chat_application/screenshots/server_running.png)

**Multiple Clients Connected:**
![Multiple Clients Connected](./part2_chat_application/screenshots/multiple_clients_connected.png)

**Wireshark Capture:**
![Wireshark Capture](./part2_chat_application/screenshots/wireshark_capture_chat.png)

---

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This project is licensed under the **MIT License**.  
See the full license in the [LICENSE](./LICENSE) file.
