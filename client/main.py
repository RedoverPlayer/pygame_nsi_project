import pygame
import pygame_gui
import json
import time
import threading

import player as p
import map as m
import tcp_socket
import udp_socket
import camera as c
import debug as d
import rich_presence
import game
import menus

from pygame.locals import (
    QUIT,
)

def main_thread(screen, udp_sock, screen_width, screen_height, cinematic, camera, map, fps, id, auth_token, rplayers, server_ip, ui_status):
    myfont = pygame.font.SysFont("freesansbold.ttf", 48)
    screen.fill((50, 50, 50))

    # loading instances
    player = p.Player(screen_width, screen_height, "Test player", (60, 60))
    running = True
    clock = pygame.time.Clock()

    main_menu = menus.MainMenu(screen_width, screen_height)
    
    # variables for on screen debug
    debug = d.Debug(player)

    # main loop
    while running:
        tick_time = clock.tick(fps)
        debug.fps += 1

        screen.fill((50, 50, 50))

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # ui manager

        pressed_keys = pygame.key.get_pressed()
        
        if ui_status[0] == "game":
            # update elements
            tiles_rendered = game.update(camera, map, player, rplayers, pressed_keys, screen, cinematic, tick_time, udp_sock, server_ip, id, auth_token)

            # debug
            if (time.time() - debug.time1) >= 1:
                debug.tick(player)
            debug.update(player, screen, myfont, tiles_rendered)
        elif ui_status[0] == "main_menu":
            main_menu.run(screen, fps, ui_status)

        # render elements to the screen
        pygame.display.flip()

if __name__ == "__main__":
    # ---- config ----
    screen_width = 1920
    screen_height = 1080

    fps = 144
    server_ip = "localhost"
    # -----------------

    # initialize pygame
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    # instantiation of important variables
    pygame.display.set_caption("NSI project")
    menus.updateThemeJson(screen_width, screen_height)
    
    cinematic = [False]
    screen = pygame.display.set_mode((screen_width, screen_height))

    map = m.Map("map1.json", 80, 60, screen_width, screen_height)
    camera = c.Camera(screen_width, screen_height, map.map_size, map.tile_size)

    rplayers = []
    ui_status = ["connecting"]

    # connect socket
    data = []
    thread_1 = threading.Thread(target=tcp_socket.connect, args=(server_ip, 12860, data, ui_status, ))
    thread_1.start()

    connection_menu = menus.ConnectionMenu(screen_width, screen_height)
    connection_menu.run(screen, fps, ui_status)

    id, auth_token, tcp_sock = data

    udp_sock = udp_socket.connect(server_ip, 12861, auth_token)
    ui_status = ["main_menu"]

    thread_2 = threading.Thread(target=tcp_socket.run, args=(tcp_sock, id, auth_token, rplayers, screen_width, screen_height, ))
    thread_3 = threading.Thread(target=udp_socket.run, args=(udp_sock, rplayers, ))

    thread_2.start()
    thread_3.start()

    try:
        rpc = rich_presence.RichPresence(825326652124430366)
        rpc.connect()
        rpc.update("En développement", "Ouais le nom du jeu est pas ouf mais en vrai ça passe")
    except:
        pass

    main_thread(screen, udp_sock, screen_width, screen_height, cinematic, camera, map, fps, id, auth_token, rplayers, server_ip, ui_status)