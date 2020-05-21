import socket
import json

headersize = 10
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1239))


full_msg = b''
new_msg = True
while True:
    msg = s.recv(16)
    if new_msg:
        msglen = int(msg[:headersize])
        print('New message, length: ' + str(msglen))
        new_msg = False
     #   msg = msg[headersize:]
    full_msg += msg
    if len(full_msg) - headersize == msglen:
        print('Full message recieved.')
        decoded = full_msg.decode('utf-8')
        noheader = decoded[headersize:]
        unpickled = json.loads(noheader)
        print(unpickled)
        new_msg = True
        full_msg = b''
