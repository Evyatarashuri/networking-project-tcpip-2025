# Report - Part 1: Encapsulation & Traffic Analysis

## 1. Introduction
This section demonstrates how application-level messages are encapsulated through the TCP/IP networking stack.
The process includes loading input messages from CSV, constructing packet headers, sending packets through a socket, and analyzing them in Wireshark.

## 2. CSV Input Structure
The input CSV contains the following columns:
- `msg_id`
- `app_protocol`
- `src_app`
- `dst_app`
- `message`
- `timestamp`

**Creation Method**
The application-level messages in the `group05_http_input.csv` file were generated using Artificial Intelligence (Gemini). The AI was prompted to create a realistic sequence of HTTP requests (GET, POST) and responses (200 OK) that follow the required schema, ensuring valid timestamps and logical flow between the `client_browser` and `web_server` applications.

![CSV Input Preview](../part1_csv_encapsulation/screenshots/csv_preview.png)


## 3. Encapsulation Workflow

When an application message is prepared for transmission, it passes through the **four layers** of the TCP/IP model.  
Each layer adds its own header, forming a complete network packet.

### **3.1 Application Layer**
- The raw message is taken directly from the CSV file (e.g., an HTTP request).
- No network headers exist yet — this is pure application data.
- Example: `GET /index.html`

### **3.2 Transport Layer (TCP)**
A TCP segment is created, containing:
- **Source port** (random high port)
- **Destination port** (8080 in this project)
- **Sequence number**
- **Acknowledgment number**
- **Flags** (SYN, ACK, PSH, FIN)
- **Window size**

**Purpose:**  
TCP ensures reliable delivery, ordering, and retransmissions.  
At this stage, the application message becomes a *TCP payload*.

### **3.3 Network Layer (IP)**
The TCP segment is wrapped inside an IPv4 header:
- **Source IP**: `127.0.0.1`
- **Destination IP**: `127.0.0.1`
- **TTL**, **Identification**, **Checksum**, **Protocol = TCP**

**Purpose:**  
IP routes the packet across networks (or loopback).  
Now we have a full **IP packet**.

### **3.4 Link Layer**
Finally, the IP packet is wrapped inside a link-layer frame:
- On loopback, Wireshark displays a **synthetic Ethernet header**
- In real networks, this includes MAC addresses and frame checksums

**Purpose:**  
Prepares the packet for physical (or virtual) transmission.

---

### Encapsulation Example (from Jupyter Notebook)

```python
Application: "GET /index.html"
Transport: "TCP Header"
Network: "IP Header"
Link: "Ethernet Header"
```

![Jupyter Notebook](../part1_csv_encapsulation/screenshots/jupyter_encapsulation_preview.png)

## 4. Packet Transmission

After building the encapsulated messages, each message is sent through a TCP socket to `127.0.0.1`.  
During the transmission Wireshark captures the packets on the loopback interface.

**What happens during transmission:**
- TCP opens a connection using the standard 3-way handshake (SYN → SYN/ACK → ACK).
- Each message from the CSV is sent as TCP payload and appears in Wireshark as a **PSH/ACK** packet.
- Wireshark shows the full path of the message: IP header → TCP header → payload.
- When the script finishes, the connection is closed with a FIN/ACK or RST (depending on how the socket is terminated).

This section demonstrates the full flow: opening the TCP session, sending data, and observing the packets in Wireshark.

### Capture Process Explanation
Wireshark was configured to listen on the loopback interface (lo0).  
Before sending the packets, a capture filter `tcp.port == 8080` was applied to record only the relevant traffic.  
Once the notebook transmitted the encapsulated messages, Wireshark captured the TCP handshake, payload packets, and connection termination.  
The resulting capture was saved as `group05_encapsulation_capture.pcapng`.


## 5. Wireshark Traffic Analysis

The traffic generated during the encapsulation process was captured using Wireshark on the **loopback interface (lo0)**.  
The capture clearly shows the full TCP/IP flow: connection setup, data transfer, and connection termination.

### **5.1 Packet Structure (Per Packet)**

Each captured packet contains the following layers:

1. **Link Layer**  
   - Wireshark displays a *synthetic* Ethernet header on loopback.  
   - Includes placeholder MAC addresses since no real Ethernet hardware is used.

2. **Network Layer (IP)**  
   - Source IP: `127.0.0.1`  
   - Destination IP: `127.0.0.1`  
   - Contains TTL, Identification, Header Length, Protocol (`TCP`), and Checksum.

3. **Transport Layer (TCP)**  
   - Source port: dynamically chosen high port  
   - Destination port: `8080` (server)  
   - Flags: SYN, ACK, PSH, FIN (depending on stage)  
   - Sequence and acknowledgment numbers, window size.

4. **Application Layer**  
   - The actual HTTP message from the CSV is visible inside the **TCP payload**.

---

### **5.2 TCP Handshake**

The first packets in the capture show the 3-way handshake:

1. **SYN** – client requests connection  
2. **SYN/ACK** – server acknowledges  
3. **ACK** – client confirms

This establishes a reliable TCP session before any application data is sent.

---

### **5.3 Data Transfer (PSH/ACK Packets)**

Packets containing the CSV-based messages appear as:

- TCP segments with **PSH** (Push) + ACK flags  
- The payload contains the HTTP request from the CSV  
- These packets correspond exactly to the encapsulation steps shown:

Application → TCP → IP → Link → Packet

Wireshark allows examining the reconstructed stream under:  
**Follow → TCP Stream**, showing the full HTTP message.

---

### **5.4 Connection Termination**

After all messages are sent, the connection is closed:

- Either via **FIN/ACK** sequence (graceful close), or  
- **RST** if the socket is closed abruptly

Wireshark shows these final control packets clearly at the end of the capture.

---

### **5.5 Summary of Observed Behavior**

The Wireshark capture verifies:

- Correct encapsulation of each CSV message  
- Proper functioning of the TCP handshake  
- Ordering and acknowledgment of packets  
- Valid payload structure inside TCP segments  
- Accurate mapping between notebook output and real network traffic

![Wireshark Capture](../part1_csv_encapsulation/screenshots/wireshark_capture_part1.jpeg)


## 6. Summary

This part shows full encapsulation and real network-level packet inspection, demonstrating how data travels through the TCP/IP model from application message → packet → Wireshark capture.
