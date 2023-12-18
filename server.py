import socket
from load_creds import load

server = socket.socket()
server.bind(load())
server.listen()
only_client, addr = server.accept()

msg = only_client.recv(1024)

print(addr, ':', msg.decode())
