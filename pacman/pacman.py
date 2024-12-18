import sys
import os
import pygame

def get_base_path():
    if getattr(sys, 'frozen', False): # executable
        return sys._MEIPASS
    else:
        return os.path.dirname(__file__)
base_path = get_base_path()
sys.path.append(os.path.join(base_path, 'classes'))

import Game_Controller

TILE_SIZE = 20
TILES_X = 27
TILES_Y = 27
SCREEN_WIDTH = TILE_SIZE * TILES_X
SCREEN_HEIGHT = TILE_SIZE * TILES_Y

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pac-man")

    game_controller = Game_Controller.Game_Controller(screen, TILE_SIZE, TILES_X, TILES_Y, SCREEN_WIDTH, SCREEN_HEIGHT)
    game_controller.setup()
    game_controller.run()
    game_controller.end()