import socket
from load_creds import load

client = socket.socket()
client.connect(load())

msg = 'Hello'.encode()
client.send(msg)
