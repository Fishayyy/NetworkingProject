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

    # Client Side 3-way Handshake
    def connect(self, address):
        print("connect!")
        self.cb.seqno = C_ISN
        self.cb.dst = address
        self.coutput.cirt_output()
        self.cinput.cirt_input()
        self.coutput.cirt_output()


    # Server Side 3-way Handshake
    def listen(self, port):
        addr = ('127.0.0.1', port)
        self.cb.sock.bind(addr)
        self.cb.state = LISTEN


    def accept(self):
        print("accept a connection!")
        self.cb.seqno = S_ISN
        self.cinput.cirt_input()
        self.coutput.cirt_output()
        self.cinput.cirt_input()  
        

    def send(self, data):
        print("send some data!")
        self.coutput.cirt_output(data)
        self.cinput.cirt_input()

    def recv(self, size):
        print("receive some data!")
        packet = self.cinput.cirt_input()
        self.coutput.cirt_output()
        return packet.data

    
    def __passive_close(self):
        self.cb.state = LAST_ACK
        self.coutput.cirt_output()  
        self.cinput.cirt_input()


    def close(self):
        if self.cb.state == CLOSE_WAIT:
            #Passive Close
            self.__passive_close()
        else:
            self.cb.state = FIN_WAIT_1
            self.coutput.cirt_output()
            packet = self.cinput.cirt_input()
            if packet.is_fin():
                # Simultaneous Close
                self.coutput.cirt_output()
                self.cinput.cirt_input()
                self.coutput.cirt_output()
            elif packet.is_ack():
                # Active Close
                self.cinput.cirt_input()
                self.coutput.cirt_output()
            elif packet.is_finack():
                self.coutput.cirt_output()

        print("we done here")
        self.cb.sock.close()
        time.sleep(2.0)
        self.cb.state = CLOSED
