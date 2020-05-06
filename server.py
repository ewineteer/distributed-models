import socket
import pickle

d = {1: 'Hey', 2:'There'}
msg = pickle.dumps(d)


HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")

    msg = bytes(f'{len(msg):{HEADERSIZE}}','utf-8') + msg

    clientsocket.send(msg)


f'{len(msg):10}'
len(msg)
f'{len(msg):10}'
