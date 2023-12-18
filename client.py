import socket
from load_creds import load_address

client = socket.socket()
client.connect(load_address())

while True:
    msg = input()
    if msg == 'q':
        client.close()
        break
    client.send(msg.encode())
