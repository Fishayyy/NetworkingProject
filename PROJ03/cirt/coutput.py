from .common import *
from .packet import Packet
import logging

logging.basicConfig(level=logging.INFO)

class Coutput:
    def __init__(self, cb):
        self.cb = cb


    def __send(self, packet, data=b''):
        logging.info(f'SEND SEQ:{packet.seqno} ACK:{packet.ackno} LEN:{len(packet.data)} CWND:{self.cb.cwnd} FLAG:{FLAG_STR[packet.flags]}')
        self.cb.sock.sendto(packet.make_packet(), self.cb.dst)
    
    
    def cirt_output(self, data=b''):
        flag = OUT_FLAGS[self.cb.state]

        packet = Packet(self.cb.seqno, self.cb.ackno, 0, flag, data)
        self.__send(packet, data)

        if self.cb.state == CLOSED:
            self.cb.seqno += 1
            self.cb.state = SYN_SENT

        elif self.cb.state == SYN_SENT:
            None

        elif self.cb.state == SYN_RECV:
            self.cb.seqno += 1

        elif self.cb.state == ESTABLISHED:
            None

        elif self.cb.state == FIN_WAIT_1:
            self.cb.seqno += 1

        elif self.cb.state == FIN_WAIT_2:
            None

        elif self.cb.state == TIME_WAIT:
            None

        elif self.cb.state == CLOSE_WAIT:
            None

        elif self.cb.state == LAST_ACK:
            self.cb.seqno += 1

        elif self.cb.state == CLOSING:
            None

        else:
            raise Exception(f'ERROR: {STATE_TO_STRING[self.cb.state]} State Insufficient for Sending')

