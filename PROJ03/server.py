import cirt.socket as cirt
import argparse

parser = argparse.ArgumentParser(description='A CIRT Server.')
parser.add_argument('-p', dest='port', default=9001, type=int, help='Port number (default 9001)')
parser.add_argument('file',help='File to serve')
args = parser.parse_args()

try:
    f = open(args.file, 'rb')
except:
    print("Cannot open file!")
    exit(1)

sock = cirt.Socket()
sock.listen(args.port)
sock.accept()

while True:
    data = f.read(500)
    if not data:
        break
    sock.send(data)
    
sock.close()