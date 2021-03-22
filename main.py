import pygame
import json
import time

import player
import map_tile

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# initialize pygame
pygame.init()
pygame.font.init()

myfont = pygame.font.SysFont('Comic Sans MS', 30)

# setting up display
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

screen.fill((50, 50, 50))

# loading player
player = player.Player(SCREEN_WIDTH, SCREEN_HEIGHT)
player_coords = [0, 0]

# loading map tiles
with open("map1.json", "r") as f:
    map = json.loads(f.read())

tile_size = 100
map_tiles = []

x_coord = 0
y_coord = 0

for y in map:
    x_coord = 0
    for x in y:
        map_tiles.append(map_tile.MapTile(SCREEN_WIDTH, SCREEN_HEIGHT, x_coord, y_coord, tile_size, x))
        x_coord += tile_size
    y_coord -= tile_size

running = True

# main loop
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False
    
    # changing player coords when pressing keys
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_q]:
        player_coords[0] -= 5
    if pressed_keys[pygame.K_d]:
        player_coords[0] += 5
    if pressed_keys[pygame.K_z]:
        player_coords[1] += 5
    if pressed_keys[pygame.K_s]:
        player_coords[1] -= 5

    # background color
    screen.fill((50, 50, 50))

    # adding map tiles to the screen
    for map_tile in map_tiles:
        map_tile.update(screen, player_coords)
    
    screen.blit(player.surf, (SCREEN_WIDTH/2 - 75/2, SCREEN_HEIGHT/2 - 75/2))

    # render elements to the screen
    pygame.display.flip()

    # calibrated for ~ 125 Hz
    time.sleep(0.008)