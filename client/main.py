from socket import socket
import pygame
import json
import time
import threading

import player as p
import map_tile
import remote_player
import udp_socket
import camera as c

from pygame.locals import (
    QUIT,
)

def main_thread(udp_sock, SCREEN_WIDTH, SCREEN_HEIGHT, rplayer):
    # initialize pygame
    pygame.init()
    pygame.font.init()

    # window title
    pygame.display.set_caption("NSI project")

    myfont = pygame.font.SysFont("freesansbold.ttf", 48)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    screen.fill((50, 50, 50))

    # loading player
    player = p.Player(SCREEN_WIDTH, SCREEN_HEIGHT, (60, 60))
    camera = c.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
    cinematic = False

    # loading map tiles
    with open("map1.json", "r") as f:
        map = json.loads(f.read())

    map_size = 60
    tile_size = 100
    map_tiles = []

    # generating map tiles
    x_coord = 0
    y_coord = 0

    for y in map:
        x_coord = 0
        for x in y:
            map_tiles.append(map_tile.MapTile(SCREEN_WIDTH, SCREEN_HEIGHT, x_coord, y_coord, tile_size, x))
            x_coord += tile_size
        y_coord += tile_size

    running = True

    clock = pygame.time.Clock()
    
    # main loop
    while running:
        # The game runs at max 144 FPS (a little less due to the time of computation of each frame)
        tick_time = clock.tick(144)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # changing player coords when pressing keys
        pressed_keys = pygame.key.get_pressed()

        # background color
        screen.fill((50, 50, 50))

        # adding map tiles to the screen
        tiles_rendered = [elem for elem in [map_tile.update(screen, camera.coords) for map_tile in map_tiles] if elem != None]

        # update elements

        rplayer.update(screen, camera.coords)
        player.update(pressed_keys, tiles_rendered, map_size, tile_size, tick_time, 2)
        if not cinematic:
            camera.update(player.coords)

        # add the player to the screen
        screen.blit(player.surf, (SCREEN_WIDTH/2 + player.coords[0] - camera.coords[0] - player.size[0]/2, SCREEN_HEIGHT/2 + player.coords[1] - camera.coords[1] - player.size[1]/2))
        udp_socket.sendCoords(udp_sock, ("localhost", 12861), player.coords)

        # debug
        playercoords = myfont.render(str(player.coords), True, (250, 250, 250))
        screen.blit(playercoords, (5, 5))
        
        tiles_number = myfont.render("Rendered tiles : " + str(len(tiles_rendered)), True, (250, 250, 250))
        screen.blit(tiles_number, (5, 50))

        # render elements to the screen
        pygame.display.flip()

def socket_receive(udp_sock, rplayer):
    while True:
        # try:
        data, addr = udp_sock.recvfrom(1024)
        data = json.loads(data.decode())
        if data["type"] == "remote_coords":
            rplayer.coords = data["coords"]
        # except:
        #     pass

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

remoteplayer = remote_player.RemotePlayer(SCREEN_WIDTH, SCREEN_HEIGHT)

# connect socket
udp_sock = udp_socket.connect("localhost", 12861)

# data_lock = threading.Lock()

thread_1 = threading.Thread(target=main_thread, args=(udp_sock, SCREEN_WIDTH, SCREEN_HEIGHT, remoteplayer, ))
thread_2 = threading.Thread(target=socket_receive, args=(udp_sock, remoteplayer, ))

thread_1.start()
thread_2.start()