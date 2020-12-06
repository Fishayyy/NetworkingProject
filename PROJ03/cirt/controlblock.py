from .common import *

class ControlBlock:
    def __init__(self):
    	# some or all of these will prove useful
        self.sock = None
        self.state = CLOSED
        self.seqno = C_ISN
        self.ackno = 0
        self.dst = () 
        self.drop = False
        self.snd_buf = b''
        self.rcv_buf = b''
        self.ack_now = False
        self.last_ack = 0
        self.dup_acks = 0
        # flow control
        self.mbuf = []
        self.snd_una = 0
        self.snd_nxt = 0
        self.snd_wnd = 0
        # congestion contorl
        self.cwnd = MSS
        self.ssthresh = 0


    def __str__(self):
        return f'[cb] state: {self.state}, seqno: {self.seqno}'