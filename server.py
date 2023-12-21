import socket
from load_creds import load_address, load_size
from player import Player, Game
from os import system
from threading import Thread
import time

server = socket.socket()
server.bind(load_address())
server.listen()
game = Game(load_size())

def player_commands(key: str, client_socket: socket) -> None:
    while True:
        direction = client_socket.recv(1024).decode()
        if direction == 'q':
            game.remove_player(key)
            break
        game.move(key, direction)

def accept_players() -> None:
    global game
    while True:
        client_socket, address = server.accept()
        key = game.add_player(client_socket, address)

        Thread(target=player_commands, args=(key, client_socket)).start()

def gameplay():
    global game
    while True:
        game.update_field()
        game.send_all()
        try:
            time.sleep(0.3)
        except KeyboardInterrupt:
            server.close()
            break

def admin():
    global game
    while True:
        game.remove_player(input())

Thread(target=accept_players).start()
Thread(target=gameplay).start()
Thread(target=admin).start()
