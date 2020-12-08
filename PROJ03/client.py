import cirt.socket as cirt

try:
    f = open("idc.jpg", 'wb')
except:
    print("Cannot open file!")
    exit(1)

sock = cirt.Socket()
sock.connect(('127.0.0.1', 9001))

while True:
    data = sock.recv(512)
    if not data:
        break
    print(data)
    f.write(data)

f.close()
sock.close()