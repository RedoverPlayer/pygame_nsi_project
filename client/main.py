from socket import socket
import pygame
import json
import time
import threading
import multiprocessing

import player as p
import map as m
import remote_player
import udp_socket
import camera as c
import debug as d

from pygame.locals import (
    QUIT,
)

def main_thread(udp_sock, screen_width, screen_height, rplayer, cinematic, camera, map, fps):
    myfont = pygame.font.SysFont("freesansbold.ttf", 48)
    screen = pygame.display.set_mode((screen_width, screen_height))

    screen.fill((50, 50, 50))

    # loading instances
    player = p.Player(screen_width, screen_height, (60, 60))

    running = True

    clock = pygame.time.Clock()
    
    # variables for on screen debug
    debug = d.Debug(player)

    # main loop
    while running:
        tick_time = clock.tick(fps)
        debug.fps += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # changing player coords when pressing keys
        pressed_keys = pygame.key.get_pressed()

        # background color
        screen.fill((50, 50, 50))

        # update elements
        tiles_rendered = map.update(camera.coords, screen)
        rplayer.update(screen, camera.coords)
        player.update(pressed_keys, tiles_rendered, map.map_size, map.tile_size, tick_time, screen, camera, 2)

        # ensure camera does not go to the border
        if not cinematic:
            camera.update(player.coords, map.map_size, map.tile_size)

        # add the player to the screens
        udp_socket.sendCoords(udp_sock, ("localhost", 12861), player.coords)

        # debug
        if (time.time() - debug.time1) >= 1:
            debug.tick(player)
        debug.update(player, screen, myfont, tiles_rendered)

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

if __name__ == "__main__":
    # initialize pygame
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    # window title
    pygame.display.set_caption("NSI project")

    # ---- config ----
    screen_width = 1920
    screen_height = 1080

    fps = 144
    tile_size = 80
    # -----------------

    cinematic = False

    remoteplayer = remote_player.RemotePlayer(screen_width, screen_height)
    map = m.Map("map1.json", tile_size, 60, screen_width, screen_height)
    camera = c.Camera(screen_width, screen_height, map.map_size, map.tile_size)

    # connect socket
    udp_sock = udp_socket.connect("localhost", 12861)

    # data_lock = threading.Lock()
    thread_1 = threading.Thread(target=main_thread, args=(udp_sock, screen_width, screen_height, remoteplayer, cinematic, camera, map, fps, ))
    thread_2 = threading.Thread(target=socket_receive, args=(udp_sock, remoteplayer, ))
    # thread_3 = threading.Thread(target=c.move_camera_to, args=((camera.width // 2 - tile_size, camera.height // 2 - tile_size), map_size, tile_size, cinematic, camera, ))

    thread_1.start()
    thread_2.start()

    time.sleep(1)
    # thread_3.start()