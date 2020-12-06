from .common import *
from .packet import Packet
import logging

logging.basicConfig(level=logging.INFO)

class Cinput:
    def __init__(self, cb):
        self.cb = cb

    def __recv(self, size):
        data, address = self.cb.sock.recvfrom(size)
        packet = Packet()
        packet.parse_packet(data)
        logging.info(f'RECV SEQ:{packet.seqno} ACK:{packet.ackno} LEN:{len(packet.data)} CWND:{self.cb.cwnd} FLAG:{FLAG_STR[packet.flags]}')
        return packet, address
    
    def cirt_input(self):
        packet, address = self.__recv(512)
