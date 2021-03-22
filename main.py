# Import the pygame module
import pygame
import json
import time

import player
import object


from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame
pygame.init()
pygame.font.init()

myfont = pygame.font.SysFont('Comic Sans MS', 30)

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

screen.fill((50, 50, 50))

player = player.Player(SCREEN_WIDTH, SCREEN_HEIGHT)
with open("map1.json", "r") as f:
    map = json.loads(f.read())

tile_size = 100
objects = []

x_coord = 0
y_coord = 0

for y in map:
    x_coord = 0
    for x in y:
        objects.append(object.Object(SCREEN_WIDTH, SCREEN_HEIGHT, x_coord, y_coord, tile_size, x))
        x_coord += tile_size
    y_coord -= tile_size

# objects.append(object.Object(SCREEN_WIDTH, SCREEN_HEIGHT, 50, 50, "wall"))
# objects.append(object.Object(SCREEN_WIDTH, SCREEN_HEIGHT, 100, 50, "wall"))

# Variable to keep the main loop running
running = True

player_coords = [0, 0]

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False
    
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_q]:
        player_coords[0] -= 5
    if pressed_keys[pygame.K_d]:
        player_coords[0] += 5
    if pressed_keys[pygame.K_z]:
        player_coords[1] += 5
    if pressed_keys[pygame.K_s]:
        player_coords[1] -= 5

    screen.fill((50, 50, 50))
    for object in objects:
        object.update(screen, player_coords)
    
    screen.blit(player.surf, (SCREEN_WIDTH/2 - 75/2, SCREEN_HEIGHT/2 - 75/2))
    pygame.display.flip()
    time.sleep(0.008)