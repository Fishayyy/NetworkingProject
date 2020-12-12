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


    def __print_err(self, expected, received):
        raise Exception(f'ERROR: Expected \"{expected}\" when in {STATE_TO_STRING[self.cb.state]} state. Recieved \"{FLAG_STR[received]}\"')

    
    def cirt_input(self):
        packet, address = self.__recv(512)

        if self.cb.state == LISTEN:
            if not packet.is_syn():
                self.__print_err("SYN", packet.flags)
            self.cb.ackno = packet.seqno + 1
            self.cb.dst = address
            self.cb.state = SYN_RECV

        elif self.cb.state == SYN_SENT:
            if packet.is_synack() == False:
                self.__print_err("SYNACK", packet.flags)
            if packet.ackno != self.cb.seqno:
                raise Exception("ACK does not match SEQ")
            self.cb.ackno = packet.seqno + 1
            self.cb.state = ESTABLISHED

        elif self.cb.state == SYN_RECV:
            if not packet.is_ack():
                self.__print_err("ACK", packet.flags)
            self.cb.state = ESTABLISHED

        elif self.cb.state == ESTABLISHED:
            if packet.is_fin():
                self.cb.state = CLOSE_WAIT
                self.cb.ackno = packet.seqno + 1
                packet.data = b''
            elif not packet.is_ack():
                self.__print_err("ACK", packet.flags)
            else:
                if len(packet.data) > 0:
                    self.cb.ackno = packet.seqno + len(packet.data)
                else:
                    if self.cb.seqno != packet.ackno:
                        raise Exception("Data was not properly acknowledged.")

        elif self.cb.state == FIN_WAIT_1:
            if packet.is_fin():
                self.cb.state = CLOSING
            elif packet.is_ack():
                self.cb.state = FIN_WAIT_2
            elif packet.is_finack():
                self.cb.state = TIME_WAIT
            else:
                self.__print_err("FIN, ACK, or FINACK", packet.flags)

        elif self.cb.state == FIN_WAIT_2:
            if not packet.is_fin():
                self.__print_err("FIN", packet.flags)
            self.cb.ackno = packet.seqno + 1
            self.cb.state = TIME_WAIT

        elif self.cb.state == LAST_ACK:
            if not packet.is_ack():
                self.__print_err("ACK", packet.flags)

        elif self.cb.state == CLOSING:
            if not packet.is_ack():
                self.__print_err("ACK", packet.flags)
                self.cb.state = TIME_WAIT

        else:
            raise Exception("Error: State Insufficient for Receiving")

        return packet
        
