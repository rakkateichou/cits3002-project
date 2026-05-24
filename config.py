# config.py


# IP Addresses (L3)

HOST_A_IP = "10.0.1.10"
HOST_B_IP = "10.0.2.20"

R1_INT1_IP = "10.0.1.1"   # Faces Host A
R1_INT2_IP = "10.0.2.1"   # Faces Host B

# MAC Addresses (L2)

HOST_A_MAC = "AA:AA:AA:AA:AA:AA"
HOST_B_MAC = "DD:DD:DD:DD:DD:DD"

R1_INT1_MAC = "BB:BB:BB:BB:BB:BB"
R1_INT2_MAC = "CC:CC:CC:CC:CC:CC"

# Routing Tables (L3)
# format: (destination_subnet, next_hop_ip, outgoing_interface)
HOST_A_ROUTING_TABLE = [
    ("10.0.2.0/24", R1_INT1_IP, "Interface 1")
]

HOST_B_ROUTING_TABLE = [
    ("10.0.1.0/24", R1_INT2_IP, "Interface 1")
]

R1_ROUTING_TABLE = [
    ("10.0.1.0/24", HOST_A_IP, "Interface 1"),
    ("10.0.2.0/24", HOST_B_IP, "Interface 2")
]

# Transport Layer Defaults (L4)

PORT_SRC = 5000
PORT_DST = 80
