# Protocol Stack Simulator (Python)

### Group Members:
*   **Ruslan Veselov** (Student ID: 24185633)
*   **Merabi Tskhadaya** (Student ID: 24202235)

---

## Project Overview

This project is a simulation of a simplified Internet protocol stack demonstrating how **Layer 2 (Data Link)**, **Layer 3 (Network)**, and **Layer 4 (Transport)** operate together to deliver application data across subnets.

## Network Topology

The network simulates two hosts in different subnets connected via a router (**R1**):

```text
[ Host A ] <-- Subnet 1 --> [ Router R1 ] <-- Subnet 2 --> [ Host B ]
```

### IP & MAC Addressing Scheme:
*   **Network 1 (Subnet 1)**: `10.0.1.0/24`
    *   **Host A**: IP `10.0.1.10` | MAC `AA:AA:AA:AA:AA:AA`
    *   **Router R1 (Interface 1)**: IP `10.0.1.1` | MAC `BB:BB:BB:BB:BB:BB`
*   **Network 2 (Subnet 2)**: `10.0.2.0/24`
    *   **Router R1 (Interface 2)**: IP `10.0.2.1` | MAC `CC:CC:CC:CC:CC:CC`
    *   **Host B**: IP `10.0.2.20` | MAC `DD:DD:DD:DD:DD:DD`

---

## Protocol Layers

### Layer 2: Data Link Layer
*   Tracks IP-to-MAC mapping locally.
*   Delivers frames connected links.

### Layer 3: Network Layer
*   Performs routing lookups.
*   Manages TTL.
*   Adds IP headers (Source IP, Destination IP, TTL)

### Layer 4: Transport Layer
*   Messages exceeding 500 bytes are segmented into multiple chunks.
*   Implements the rdt2.2 protocol.
*   Checksum validation at receiver nodes.

---

## Running the Simulation

The simulation accepts the application message size (in bytes) as a command-line argument.

To run the simulation with standard `python`:

```bash
python main.py <message_size>
```

### Examples:

1.  **10-Byte Message**:
    ```bash
    python main.py 10
    ```
2.  **600-Byte Message (Triggers Segmentation)**:
    ```bash
    python main.py 600
    ```
