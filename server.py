import socket
from load_creds import load_address, load_size
from player import Player, Game
from os import system

server = socket.socket()
server.bind(load_address())
server.listen()
game = Game(load_size())

client_socket, address = server.accept()

player = Player(client_socket, address)
key = game.add_player(player)

while True:
    print(game.field)
    try:
        msg = client_socket.recv(1024).decode()
    except KeyboardInterrupt:
        server.close()
        server.shutdown()
        break

    if msg == 'q':
        game.remove_player(key)
        server.close()
        server.shutdown()
        break
    player.move(msg)
    game.update_field()
    system('clear')
