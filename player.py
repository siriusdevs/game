from socket import socket
import random
import time
from typing import Self


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
            color: tuple[int],
            x: int = 0,
            y: int = 0,
            lifes: int = 3,
    ) -> None:
        self.socket = cl_socket
        self.addr = addr
        self.x = x
        self.y = y
        self.lifes = lifes
        self.color = color

    def move(self, direction: str):
        if direction not in self._moves.keys():
            return
        to_move = self._moves[direction]
        self.x += to_move[0]
        self.y += to_move[1]

    def __str__(self) -> str:
        return f'{self.lifes};{self.color[0]},{self.color[1]},{self.color[2]};{self.x},{self.y}'
    
    @classmethod
    def from_str(cls, raw: str) -> Self:
        lifes, color, position = raw.split(';')
        lifes = int(lifes)
        color = tuple([int(color) for color in color.split(',')])
        position = tuple([int(pos) for pos in position.split(',')])
        return cls(None, None, color, position[0], position[1], lifes)




class Modifier:
    symbol: str

    def __init__(self, field_width: int, field_height: int) -> None:
        self.x = random.randint(1, field_width-1)
        self.y = random.randint(1, field_height-1)


class Heart(Modifier):
    symbol = chr(10084)

class ColorGenerator:
    _color_range = 0, 255

    def __init__(self) -> None:
        self.__used_colors = []

    def generate(self) -> tuple[int]:
        return (
            random.randint(*self._color_range),
            random.randint(*self._color_range),
            random.randint(*self._color_range),
        )

    def get(self) -> tuple[int]:
        color = self.generate()
        while color in self.__used_colors: # TODO similar colors check
            color = self.generate()
        return color

    def remove_color(self, color: tuple[int]) -> None:
        self.__used_colors.remove(color)


class Game:
    _modifier_interval = 10

    def __init__(self, size: tuple[int, int]) -> None:
        self._time = time.time()
        self._current_id = 0
        self._color_generator = ColorGenerator()
        self.width, self.height = size[0], size[1]
        self._players: dict[int, Player] = {}
        self._modifiers: list[Modifier] = []

    def add_player(self, player_socket: socket, address: tuple) -> str:
        color = self._color_generator.get()
        player = Player(player_socket, address, color)
        player_id = self._current_id
        self._players[player_id] = player
        self._current_id += 1
        return player_id

    def remove_player(self, id_: int) -> None:
        if id_ in self._players.keys():
            self._players[id_].socket.close()
            del self._players[id_]

    def check_collision(self, key: int) -> None:
        player = self._players[key]
        if player.x == 0 and player.y == 0:
            return
        for current_key, current in self._players.items():
            if current != player:
                if current.x == player.x and current.y == player.y:
                    self.damage(player, key)
                    self.damage(current, current_key)
                    break
        for modifier in self._modifiers:
            if modifier.x == player.x and modifier.y == player.y:
                if isinstance(modifier, Heart):
                    self.add_life(player)
                    self._modifiers.remove(modifier)

    def add_life(self, player: Player):
        player.lifes += 1
    
    def damage(self, player: Player, key: int):
        player.lifes -= 1
        if player.lifes <= 0:
            self.remove_player(key)

    def move(self, key: int, direction: str) -> None:
        player = self._players[key]
        player.move(direction)
        player.x %= self.width
        player.y %= self.height
        self.check_collision(key)

    def update_field(self) -> None:
        if time.time() > self._time + self._modifier_interval:
            self._modifiers.append(Heart(self.width, self.height))
            self._time = time.time()

    def send_all(self) -> None:
        message = str(self)
        print(message)
        for player in self._players.values():
            player.socket.send(message.encode())

    def __str__(self) -> str:
        return '|'.join([str(player) for player in self._players.values()])
