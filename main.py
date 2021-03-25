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

# window title
pygame.display.set_caption("NSI project")

myfont = pygame.font.SysFont("freesansbold.ttf", 48)

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

map_size = 60
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

clock = pygame.time.Clock()

# main loop
while running:
    # The game runs at max 144 FPS (a little less due to the time of computation of each frame)
    tick_time = clock.tick(144)

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

    # changing player coords when pressing keys
    pressed_keys = pygame.key.get_pressed()
    movement_speed = 2 * tick_time / 8
    if pressed_keys[pygame.K_q]:
        if player_coords[0] - movement_speed > 38:
            player_coords[0] -= movement_speed
        else:
            player_coords[0] -= player_coords[0] - 38
    if pressed_keys[pygame.K_d]:
        if player_coords[0] + movement_speed < map_size * tile_size - 38:
            player_coords[0] += movement_speed
        else:
            player_coords[0] -= player_coords[0] - (map_size * tile_size - 38)
    if pressed_keys[pygame.K_z]:
        if player_coords[1] - movement_speed > 38:
            player_coords[1] -= movement_speed
        else:
            player_coords[1] -= player_coords[1] - 38
    if pressed_keys[pygame.K_s]:
        if player_coords[1] + movement_speed < map_size * tile_size - 38:
            player_coords[1] += movement_speed
        else:
            player_coords[1] -= player_coords[1] - (map_size * tile_size - 38)

    # background color
    screen.fill((50, 50, 50))

    # adding map tiles to the screen
    tiles_rendered = [elem for elem in [map_tile.update(screen, player_coords) for map_tile in map_tiles] if elem != None]

    # for map_tile in tiles_rendered:
    #     if player.rect.colliderect(map_tile.rect):
    #         if map_tile.type == "wall":
    #             print("hey")

    screen.blit(player.surf, (SCREEN_WIDTH/2 - 75/2, SCREEN_HEIGHT/2 - 75/2))

    # debug
    playercoords = myfont.render(str(player_coords), True, (250, 250, 250))
    screen.blit(playercoords, (5, 5))
    
    tiles_number = myfont.render("Rendered tiles : " + str(len(tiles_rendered)), True, (250, 250, 250))
    screen.blit(tiles_number, (5, 50))

    # render elements to the screen
    pygame.display.flip()

    # calibrated for 100 Hz
    # time.sleep(0.01)