import socket
from .packet import Packet
from .common import *
from .controlblock import ControlBlock
from .coutput import Coutput
from .cinput import Cinput
import logging
import time

class Socket:
    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.cb = ControlBlock()
        self.cb.sock = sock
        self.coutput = Coutput(self.cb)
        self.cinput = Cinput(self.cb)
        

    ##################################################################
    # API Calls - used by the client and server.
    # All your hard work is hidden by these few functions.
    # Let's take a moment to thank everyone who has worked on
    # implementing TCP for our respective operating systems.
    ##################################################################

    def await_ack(self):
        packet, address = self.cinput.cirt_input()  
        if not packet.is_ack():
            raise Exception("Expected ACK")
        return packet, address


    def await_syn(self):
        packet, address = self.cinput.cirt_input()
        if not packet.is_syn():
            raise Exception("Expected SYN")
        return packet, address


    def recv_ack(self):
        packet, _ = self.cinput.cirt_input()
        if packet.is_fin():
            self.cb.drop = True
        elif not packet.is_ack():
            raise Exception("Expected ACK")
        return packet


    # Client Side 3-way Handshake
    def connect(self, address):
        print("connect!")
        self.cb.seqno = C_ISN
        self.cb.dst = address
        self.coutput.cirt_output()
        self.cb.state = SYN_SENT
        packet, address = self.cinput.cirt_input()
        if not packet.is_synack():
            raise Exception("Expected SYNACK")
        self.cb.ackno = packet.seqno + 1
        self.cb.seqno += 1
        self.cb.state = ESTABLISHED
        self.coutput.cirt_output()


    # Server Side 3-way Handshake
    def listen(self, port):
        addr = ('127.0.0.1', port)
        self.cb.sock.bind(addr)
        self.cb.state = LISTEN


    def accept(self):
        print("accept a connection!")
        self.cb.seqno = S_ISN
        packet, address = self.cinput.cirt_input()
        if not packet.is_syn():
            raise Exception("Expected SYN")
        self.cb.ackno = packet.seqno + 1
        self.cb.dst = address
        self.cb.state = SYN_RECV
        self.coutput.cirt_output()
        packet, address = self.cinput.cirt_input()  
        if not packet.is_ack():
            raise Exception("Expected ACK")
        self.cb.seqno += 1
        self.cb.state = ESTABLISHED
        

    def send(self, data):
        if self.cb.state != ESTABLISHED:
            return
        print("send some data!")
        self.coutput.cirt_output(data)
        packet, _ = self.cinput.cirt_input()
        if packet.is_fin():
            self.cb.drop = True 
        elif not packet.is_ack():
            raise Exception("Expected ACK")


    def recv(self, size):
        if self.cb.state != ESTABLISHED:
            return b''
        print("receive some data!")
        packet, _ = self.cinput.cirt_input() 
        if packet.is_fin():
            self.cb.drop = True 
            return b''
        elif not packet.is_ack():
            raise Exception("Expected ACK")
        self.coutput.cirt_output()
        return packet.data

    
    def __passive_close(self):
        self.coutput.cirt_output()
        self.cb.state = CLOSE_WAIT
        self.coutput.cirt_output()
        self.cb.state = LAST_ACK        
        packet, _ =self.cinput.cirt_input()
        if not packet.is_ack():
            raise Exception("Expected ACK")


    def close(self):
        if self.cb.drop:
            self.__passive_close()
        else:
            self.cb.state = FIN_WAIT_1
            self.coutput.cirt_output()
            packet, _ = self.cinput.cirt_input()
            if packet.is_fin():
                # Simultaneous Close
                self.cb.state = CLOSING
                self.coutput.cirt_output()
                packet, _ = self.cinput.cirt_input()
                if not packet.is_ack():
                    raise Exception("Expected ACK")
                self.cb.state = TIME_WAIT
                self.coutput.cirt_output()
            if packet.is_finack():
                self.cb.state = TIME_WAIT
                self.coutput.cirt_output()
            if packet.is_ack():
                self.cb.state = FIN_WAIT_2
                packet, _ = self.cinput.cirt_input()
                if not packet.is_fin():
                    raise Exception("Expected FIN")
                self.cb.state = TIME_WAIT
                self.coutput.cirt_output()
            else:
                #TODO: Re-send 3 times before dropping
                raise Exception("Expected FIN, ACK, or FINACK")

        print("we done here")
        self.cb.sock.close()
        time.sleep(2.0)
        self.cb.state = CLOSED
