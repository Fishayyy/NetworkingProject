from .common import *
from .packet import Packet
import logging

logging.basicConfig(level=logging.INFO)

class Coutput:
    def __init__(self, cb):
        self.cb = cb


    def __send(self, packet):
        logging.info(f'SEND SEQ:{packet.seqno} ACK:{packet.ackno} LEN:{len(packet.data)} CWND:{self.cb.cwnd} FLAG:{FLAG_STR[packet.flags]}')
        self.cb.sock.sendto(packet.make_packet(), self.cb.dst)
    
    
    def cirt_output(self):
        flag = OUT_FLAGS[self.cb.state]

        packet = Packet(self.cb.seqno, self.cb.ackno, 0, flag, b'')
        self.__send(packet)
