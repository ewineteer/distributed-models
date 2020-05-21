import socket
import json


headersize = 10
data = {1:'Hey',2:'There'}
msg = json.dumps(data)



header=str(len(msg))
spaces = headersize - len(header)
header = header.ljust(headersize)

sendready = bytes(header + msg, 'utf-8')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1239))
s.listen(5)

while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")

    clientsocket.send(sendready)
