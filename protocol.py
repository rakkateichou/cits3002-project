# protocol.py

class L4Segment:
    """ Layer 4: Transport Layer (UDP-like Segment) """
    def __init__(self, src_port, dst_port, type_flag, seq_num, data, checksum=0):
        self.src_port = src_port
        self.dst_port = dst_port
        self.type_flag = type_flag   # 0 = DATA, 1 = ACK
        self.seq_num = seq_num       # 0 or 1 (Alternating Bit)
        self.data = data             # Application message payload
        self.length = 8 + len(data) if data else 8  # 8 bytes header + data size
        self.checksum = checksum     # Teammate 2 will calculate this

class L3Packet:
    """ Layer 3: Network Layer (IP-like Packet) """
    def __init__(self, src_ip, dst_ip, ttl, protocol, payload):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.ttl = ttl               # Starts at 100
        self.protocol = protocol     # 17 = UDP
        self.payload = payload       # The L4Segment goes here
        self.total_length = 20 + payload.length

class L2Frame:
    """ Layer 2: Data Link Layer (Ethernet-like Frame) """
    def __init__(self, src_mac, dst_mac, eth_type, payload):
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.eth_type = eth_type     # "0x0800" for IPv4
        self.payload = payload       # The L3Packet goes here
