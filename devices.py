# devices.py
import config
from protocol import L2Frame, L3Packet, L4Segment

class Node:
    """ Base class for Hosts and Routers """
    def __init__(self, name):
        self.name = name
        self.mac_table = {}  # Maps IP -> MAC
    
    def log(self, layer, message):
        """ Formatting helper to match PDF output logs perfectly """
        print(f"{self.name}: Layer {layer}: {message}")


class Host(Node):
    def __init__(self, name, ip, mac, default_gateway_ip, gateway_mac):
        super().__init__(name)
        self.ip = ip
        self.mac = mac
        self.default_gateway_ip = default_gateway_ip
        
        # Pre-populate MAC table with the gateway (simplifies ARP for logical sim)
        self.mac_table[default_gateway_ip] = gateway_mac 
        
        # Link to directly connected device (Router)
        self.link = None 

        # New states for L4 (MT)
        self.next_seq_num = 0
        self.expected_seq_num = 0
        self.waiting_for_ack = False
        self.last_ack_received = None

    # ==========================================
    # LAYER 3: NETWORK
    # ==========================================
    def send_network(self, segment, dst_ip):
        """ Encapsulate Segment into Packet, determine routing, pass to L2 """
        self.log(3, f"Segment received from Transport Layer: SRC_IP={self.ip}, DST_IP={dst_ip}, TTL=100")
        self.log(3, f"Destination IP read: {dst_ip}")
        self.log(3, "Routing table lookup performed")
        
        next_hop_ip = self.default_gateway_ip
        self.log(3, f"Next-hop IP determined: {next_hop_ip}")
        self.log(3, "Outgoing interface selected")
        
        # Encapsulate
        packet = L3Packet(self.ip, dst_ip, 100, 17, segment)
        self.log(3, "Packet forwarded to Data Link Layer")
        
        self.send_datalink(packet, next_hop_ip)

    def receive_network(self, packet):
        """ Decapsulate Packet, check IP, pass Segment to L4 """
        self.log(3, f"Packet received from Data Link Layer: SRC_IP={packet.src_ip}, DST_IP={packet.dst_ip}, TTL={packet.ttl}")
        self.log(3, f"Destination IP read: {packet.dst_ip}")
        
        if packet.dst_ip == self.ip:
            self.log(3, "Packet identified as local delivery")
            self.log(3, "Segment delivered to Transport Layer")
            self.receive_transport(packet.payload) # Hand off to Teammate 2's L4 logic
        else:
            self.log(3, "Packet dropped: Invalid destination IP")

    # ==========================================
    # LAYER 2: DATA LINK
    # ==========================================
    def send_datalink(self, packet, next_hop_ip):
        """ Encapsulate Packet into Frame, do MAC lookup, send over wire """
        self.log(2, "Packet received from Network Layer")
        dst_mac = self.mac_table.get(next_hop_ip, "UNKNOWN")
        self.log(2, f"Destination MAC lookup for next-hop IP ({next_hop_ip}) → {dst_mac}")
        
        # Encapsulate
        frame = L2Frame(self.mac, dst_mac, "0x0800", packet)
        self.log(2, f"Frame created: SRC_MAC={self.mac}, DST_MAC={dst_mac}")
        self.log(2, "Frame sent")
        
        # Send physical frame to link (Router)
        self.link.receive_datalink(frame)

    def receive_datalink(self, frame):
        """ Decapsulate Frame, pass Packet to L3 """
        self.log(2, "Frame received")
        self.log(2, f"Source MAC learned: {frame.src_mac}")
        
        # Simple logical MAC learning
        # (In a real network, we'd learn IP from ARP, but logic dictates we log it)
        
        self.log(2, "Packet delivered to Network Layer")
        self.receive_network(frame.payload)

    # ==========================================
    # LAYER 4: TRANSPORT (Teammate 2's Domain)
    # ==========================================
    def send_transport(self, message_data):
        # TODO: Teammate 2
        # 1. Segment message if > 500 bytes.
        # 2. Implement RDT 2.2 loop (Wait for correct ACK, timeout/retransmit logic).
        # 3. Calculate checksum.
        # 4. Call self.send_network(segment, config.HOST_B_IP)

        self.log(4, "Message received from Application layer")

        # Splitting message into chunks of 500 bytes
        chunks = [message_data[i:i + 500] for i in range (0, len(message_data), 500)]

        self.log(4, f"Message splitted into {len(chunks)} chunks")

        for chunk in chunks:
            ack_received = False

            while not ack_received:
                seq_num = self.next_seq_num

                segment = L4Segment(
                    src_port = config.PORT_SRC,
                    dst_port = config.PORT_DST,
                    type_flag = 0, # 0 -> DATA
                    seq_num = seq_num,
                    data = chunk,
                    checksum = 0 # initial checksum 0
                )
        
                segment.checksum = self.calculate_checksum(segment) # Checksum assigning

                self.waiting_for_ack = True
                self.last_ack_received = None

                self.log(4, f"DATA segment created: SEQ = {seq_num}, LENGTH = {segment.length}, CHECKSUM = {segment.checksum}")
                self.log(4, "Segment was sent to Network LAyer")

                self.send_network(segment, self.get_peer_ip())


                if self.last_ack_received == seq_num:
                    self.log(4, f"Correct ACK received: ACK: {self.last_ack_received}")
                    self.waiting_for_ack = False
                    ack_received = True

                    self.next_seq_num = 1 - self.next_seq_num
                else:
                    self.log(4, "Incorrect of missing ACK. Retransmitting the segment")

    def calculate_checksum(self, segment): # basic checksum
        data_string = ( 
            str(segment.src_port)
            + str(segment.dst_port)
            + str(segment.type_flag)
            + str(segment.seq_num)
            + str(segment.data)
        )

        return sum(ord(char) for char in data_string) % 256
    
    def get_peer_ip(self): #getter of other Host IP so can work bothways
        if self.ip == config.HOST_A_IP:
            return config.HOST_B_IP
        else:
            return config.HOST_A_IP

    def receive_transport(self, segment):
        # TODO: Teammate 2
        # 1. Verify Checksum.
        # 2. If DATA segment: Deliver data to App layer, generate ACK, send_network(ack_segment)
        # 3. If ACK segment: Process sequence number to continue RDT 2.2

        if segment.type_flag == 0:
            segment_type = "DATA"
        else: 
            segment_type = "ACK" 

        self.log(4, f"Segment received from Network layer: TYPE = {segment_type}, SEQ = {segment.seq_num}")

        # Checksumm verification block
        received_checksum = segment.checksum
        segment.checksum = 0
        expected_checksum = self.calculate_checksum(segment)
        segment.checksum = received_checksum

        if received_checksum != expected_checksum:
            self.log(4, "Failed to validate checksum")

            duplicate_ack_num = 1 - self.expected_seq_num

            ack_segment = L4Segment(
                src_port = config.PORT_DST,
                dst_port = config.PORT_SRC,
                type_flag = 1, # 1 -> ACK msg
                seq_num = duplicate_ack_num,
                data = "",
                checksum = 0 # initial checksum 0
            )

            ack_segment.checksum = self.calculate_checksum(ack_segment)

            self.log(4, f"Duplicate ACK created: ACK = {duplicate_ack_num}")

            self.send_network(ack_segment, self.get_peer_ip())
            self.log(4, "ACK was sent to Network layer")
            
            return 
        
        self.log(4, "Checksum validations successful")


        # First Transfer case
        if segment.type_flag == 0:
            self.log(4, f"Segment with DATA received: SEQ={segment.seq_num}")
        
            if segment.seq_num == self.expected_seq_num:
                self.log(4, "SEQ num is correct")
                self.log(4, f"Data will be transferred to Application layer: {segment.data}")

                ack_segment = L4Segment(
                    src_port = config.PORT_DST,
                    dst_port = config.PORT_SRC,
                    type_flag = 1, # 1 -> ACK msg
                    seq_num = segment.seq_num,
                    data = "",
                    checksum = 0 # initial checksum 0
                )
                
                #checksum validation
                ack_segment.checksum = self.calculate_checksum(ack_segment)
                self.log(4, f"ACK created: ACK = {segment.seq_num}")
                self.log(4, "ACK segment sent to NEtwork layer")

                self.send_network(ack_segment, self.get_peer_ip()) #sending ack back to sender
                self.expected_seq_num = 1 - self.expected_seq_num
            else: # traceback to last correct ack that was received
                self.log(4, "Unexpected data segment was received")

                duplicate_ack_num = 1 - self.expected_seq_num
                ack_segment = L4Segment(
                    src_port = config.PORT_DST,
                    dst_port = config.PORT_SRC,
                    type_flag = 1, # 1 -> ACK msg
                    seq_num = duplicate_ack_num,
                    data = "",
                    checksum = 0 # initial checksum 0
                )

                ack_segment.checksum = self.calculate_checksum(ack_segment)

                self.log(4, f"Dupe ACK created: ACK = {duplicate_ack_num}")

                self.send_network(ack_segment, self.get_peer_ip())
                self.log(4, "Dupe of ACK was sent to Network layer")
        # Second transfer case
        elif segment.type_flag == 1:
            self.log(4, f"ACK segment receved: ACK = {segment.seq_num}")
            
            if self.waiting_for_ack:
                self.last_ack_received = segment.seq_num
                self.log(4, f"ACK processed: ACK = {segment.seq_num}")
            else:
                self.log(4, "ACK ignored. No segment awaiting an ACK at the moment")


class Router(Node):
    def __init__(self, name):
        super().__init__(name)
        # Define router interfaces natively
        self.interfaces = {
            "Interface 1": {"ip": config.R1_INT1_IP, "mac": config.R1_INT1_MAC, "link": None},
            "Interface 2": {"ip": config.R1_INT2_IP, "mac": config.R1_INT2_MAC, "link": None}
        }
        # Pre-fill router MAC tables so it knows how to reach directly connected hosts
        self.mac_table[config.HOST_A_IP] = config.HOST_A_MAC
        self.mac_table[config.HOST_B_IP] = config.HOST_B_MAC

    def receive_datalink(self, frame):
        # Determine which interface the frame physically came in on
        if frame.src_mac == config.HOST_A_MAC:
            incoming_int = "Interface 1"
        elif frame.src_mac == config.HOST_B_MAC:
            incoming_int = "Interface 2"
        else:
            incoming_int = "Unknown Interface"

        self.log(2, f"Frame received on {incoming_int}")
        self.log(2, f"Source MAC learned: {frame.src_mac} on {incoming_int}")
        self.log(2, "Packet delivered to Network Layer")
        
        self.receive_network(frame.payload)

    def receive_network(self, packet):
        self.log(3, f"Packet received from Data Link Layer: SRC_IP={packet.src_ip}, DST_IP={packet.dst_ip}, TTL={packet.ttl}")
        self.log(3, f"Destination IP read: {packet.dst_ip}")
        
        # TTL decrement
        old_ttl = packet.ttl
        packet.ttl -= 1
        self.log(3, f"TTL decremented: {old_ttl} → {packet.ttl}")
        
        if packet.ttl <= 0:
            self.log(3, "Packet dropped due to TTL expiry")
            return

        self.log(3, "Routing table lookup performed")
        
        # Simulated routing table (Destination Network check)
        if packet.dst_ip == config.HOST_A_IP:
            next_hop_ip = config.HOST_A_IP
            out_iface = "Interface 1"
        elif packet.dst_ip == config.HOST_B_IP:
            next_hop_ip = config.HOST_B_IP
            out_iface = "Interface 2"
        else:
            self.log(3, "No route found, packet dropped")
            return

        self.log(3, f"Next-hop IP determined: {next_hop_ip}")
        self.log(3, f"Outgoing interface selected ({out_iface})")
        self.log(3, "Packet forwarded to Data Link Layer")
        
        self.send_datalink(packet, next_hop_ip, out_iface)

    def send_datalink(self, packet, next_hop_ip, out_iface):
        self.log(2, "Packet received from Network Layer")
        dst_mac = self.mac_table.get(next_hop_ip, "UNKNOWN")
        self.log(2, f"Destination MAC lookup for next-hop IP ({next_hop_ip}) → {dst_mac}")
        
        src_mac = self.interfaces[out_iface]["mac"]
        
        # Encapsulate
        frame = L2Frame(src_mac, dst_mac, "0x0800", packet)
        self.log(2, f"Frame created: SRC_MAC={src_mac}, DST_MAC={dst_mac}")
        self.log(2, f"Frame forwarded on {out_iface}")
        
        # Push over the physical wire to connected node
        target_node = self.interfaces[out_iface]["link"]
        if target_node:
            target_node.receive_datalink(frame)
