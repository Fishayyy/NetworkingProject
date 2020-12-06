from .common import *

class Packet:
    def __init__(self, seqno=0, ackno=0, win=0, flags=0, data=b''):
        self.seqno = seqno
        self.ackno = ackno
        self.win = win
        self.flags = flags
        self.data = data


    def make_packet(self):
        packet = self.seqno.to_bytes(4, byteorder='big', signed=True) \
                + self.ackno.to_bytes(4, byteorder='big', signed=True) \
                + self.win.to_bytes(2, byteorder='big', signed=True) \
                + b'\x00' + self.flags.to_bytes(1, byteorder='big', signed=True) \
                + self.data
        return packet


    def parse_packet(self, packet):
        self.seqno = int.from_bytes(packet[:4], byteorder='big', signed=True)
        self.ackno = int.from_bytes(packet[4:8], byteorder='big', signed=True)
        self.win = int.from_bytes(packet[8:10], byteorder='big', signed=True)
        self.flags = int.from_bytes(packet[11:12], byteorder='big', signed=True)
        self.data = packet[12:]


    def is_syn(self):
        return self.flags == SYN
    

    def is_ack(self):
        return self.flags == ACK

    def is_fin(self):
        return self.flags == FIN

    def is_synack(self):
        return self.flags == SYNACK
        
    def __str__(self):
        return f'seq:{self.seqno}, ack:{self.ackno}, win:{self.win}, flags:{self.flags} data:\n{self.data}\n'
