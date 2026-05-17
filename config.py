# config.py

# ==========================================
# IP Addresses (Layer 3)
# ==========================================
HOST_A_IP = "10.0.1.10"
HOST_B_IP = "10.0.2.20"

R1_INT1_IP = "10.0.1.1"   # Faces Host A
R1_INT2_IP = "10.0.2.1"   # Faces Host B

# ==========================================
# MAC Addresses (Layer 2)
# ==========================================
HOST_A_MAC = "AA:AA:AA:AA:AA:AA"
HOST_B_MAC = "DD:DD:DD:DD:DD:DD"

R1_INT1_MAC = "BB:BB:BB:BB:BB:BB"
R1_INT2_MAC = "CC:CC:CC:CC:CC:CC"

# ==========================================
# Transport Layer Defaults (Layer 4)
# ==========================================
PORT_SRC = 5000
PORT_DST = 80
