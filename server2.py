import socket
import pickle

d = {1:'Hey',2:'There'}
msg = pickle.dumps(d)

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 1236))
s.listen(5)

while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")

    msg = pickle.dumps(d)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}",'utf-8')+msg

    clientsocket.send(msg)
