import cirt.socket as cirt

sock = cirt.Socket()
sock.connect(('127.0.0.1', 9001))

while True:
    data = sock.recv(512)
    if not data:
        break
    print(data)

sock.close()