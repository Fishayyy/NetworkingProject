### Flags
SYN = 0x01     # 0000 0001
ACK = 0x02     # 0000 0010
SYNACK = 0x03  # 0000 0011
FIN = 0x04     # 0000 0100
ERR = 0x08     # 0000 1000
FLAG_STR = ("NONE","SYN","ACK","SYNACK","FIN","","","","ERR")

### CIRT States
CLOSED = 0
LISTEN = 1
SYN_SENT = 2
SYN_RECV = 3
ESTABLISHED = 4
FIN_WAIT_1 = 5
FIN_WAIT_2 = 6
TIME_WAIT = 7
CLOSE_WAIT = 8
LAST_ACK = 9

### Out Flags Based on State
OUT_FLAGS = (
    SYN,    # CLOSED
    0,      # LISTEN
    ACK,    # SYN_SENT
    SYNACK, # SYN_RECV
    ACK,    # ESTABLISHED
    FIN,    # FIN-WAIT-1
    0,      # FIN-WAIT-2
    ACK,    # TIME-WAIT
    ACK,    # CLOSE_WAIT
    0       # LAST_ACK
    )

### CB Info
C_ISN = 2501
S_ISN = 1337

### Flow Control/Congestion Avoidance
MSS = 500   # 500 + 12 byte header = 512 bytes