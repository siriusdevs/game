from socket import socket
import random


class Player:
    _moves = {
        'd': (1, 0),
        'w': (0, -1),
        'a': (-1, 0),
        's': (0, 1),
    }

    def __init__(
            self, 
            cl_socket: socket, 
            addr: tuple[str, int],
    ) -> None:
        self.socket = cl_socket
        self.addr = addr
        self.x = 0
        self.y = 0
        self.lifes = 3

    def move(self, direction: str):
        if direction not in self._moves.keys():
            return
        to_move = self._moves[direction]
        self.x += to_move[0]
        self.y += to_move[1]

class Game:
    def __init__(self, size: tuple[int, int]) -> None:
        self._symbols = [chr(i) for i in range(45, 127)]
        self.width, self.height = size[0], size[1]
        self._players = {}
        self._field = []
        for _ in range(self.height):
            self._field.append([' '] * self.width)

    def add_player(self, player: Player) -> str:
        random_idx = random.randint(0, len(self._symbols)-1)
        symbol = self._symbols.pop(random_idx)
        self._players[symbol] = player
        return symbol

    def remove_player(self, symbol: str) -> None:
        if symbol in self._players.keys():
            self._symbols.append(symbol)
            del self._players[symbol]
    
    def clear_field(self) -> None:
        self._field = [[' '] * self.width for _ in range(self.height)]

    def check_collision(self, key: str) -> None:
        player = self._players[key]
        if player.x == 0 and player.y == 0:
            return
        for current in self._players.values():
            if current != player:
                if current.x == player.x and current.y == player.y:
                    self.damage(player, key)
                    break
    
    def damage(self, player: Player, key: str):
        player.lifes -= 1
        if player.lifes <= 0:
            self.remove_player(key)

    def move(self, player_key: str, direction: str) -> None:
        player = self._players[player_key]
        player.move(direction)
        player.x %= self.width
        player.y %= self.height
        self.check_collision(player)

    def update_field(self) -> None:
        self.clear_field()
        for key, player in self._players.items():
            self._field[player.y][player.x] = key

    @property
    def field(self) -> list[list[str]]:
        field = '\n'.join(['|' + ''.join(line) + '|' for line in self._field])
        bar = '-' * self.width
        lifes = [f'{key}{player.lifes}' for key, player in self._players.items()]
        return '\n'.join([bar, field, bar, lifes])
