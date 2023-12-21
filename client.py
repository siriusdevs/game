import socket
from load_creds import load_address, load_size
import pygame
from pygame.locals import *
from pygamelib import *
from player import Player


UNIT_SIZE = 20
SIZE = load_size() # in units count
BLACK = 0, 0, 0
EXIT_MSG = 'q'
WIDTH, HEIGHT = UNIT_SIZE * SIZE[0] + 2, UNIT_SIZE * SIZE[1]

class App:
    """Create a single-window app with multiple scenes."""
    def __init__(self):
        """Initialize pygame and the application."""
        pygame.init()
        App.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        App.running = True


class Visualizer(App):
    _arrows = {
        K_UP: 'w',
        K_DOWN: 's',
        K_LEFT: 'a',
        K_RIGHT: 'd',
    }

    def __init__(self, server: socket):
        super().__init__()
        self._players = []
        self.bg_color = BLACK
        self.server = server
 
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    self.server.send(EXIT_MSG.encode())
                    pygame.quit()

                if event.type == KEYDOWN:
                    if event.key in self._arrows.keys():
                        self.server.send(self._arrows[event.key].encode())

            self.update(self.server.recv(1024).decode())
            self.draw()

    def update(self, message: str) -> None:
        print(message)
        self._players = list(map(Player.from_str, message.split('|')))

    def rect_from_player(self, player: Player) -> None:
        return Rect(player.x * UNIT_SIZE, player.y * UNIT_SIZE, UNIT_SIZE, UNIT_SIZE)

    def draw_text(self, text, pos):
        font = pygame.font.Font(None, 24)
        img = font.render(text, True, BLACK)
        self.screen.blit(img, pos)

    def draw_players(self) -> None:
        height_count = 0
        for player in self._players:
            pygame.draw.rect(self.screen, player.color, self.rect_from_player(player))
            position = WIDTH - UNIT_SIZE, height_count * UNIT_SIZE 
            rect = Rect(*position, UNIT_SIZE, UNIT_SIZE)
            pygame.draw.rect(self.screen, player.color,rect)
            self.draw_text(str(player.lifes), position)
            height_count += 1

    def draw(self) -> None:
        self.screen.fill(self.bg_color)
        self.draw_players()
        pygame.display.flip()
                
if __name__ == '__main__':
    client = socket.socket()
    client.connect(load_address())
    Visualizer(client).run()

    client.close()
