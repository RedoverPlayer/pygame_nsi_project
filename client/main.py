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

def main_thread(screen, udp_sock, screen_width, screen_height, cinematic, camera, map, fps, id, auth_token, rplayers, server_ip):
    myfont = pygame.font.SysFont("freesansbold.ttf", 48)
    screen.fill((50, 50, 50))

    # loading instances
    player = p.Player(screen_width, screen_height, "Test player", (60, 60))
    running = True
    ui_status = "main_menu"
    clock = pygame.time.Clock()

    title, play_button = menus.mainMenu(screen_width, screen_height, manager)
    
    # variables for on screen debug
    debug = d.Debug(player)

    # main loop
    while running:
        tick_time = clock.tick(fps)
        debug.fps += 1

        screen.fill((50, 50, 50))

        for event in pygame.event.get():
            manager.process_events(event)
                
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == play_button:
                        ui_status = "game"

            if event.type == QUIT:
                running = False

        # ui manager
        if ui_status  == "main_menu":
            manager.update(tick_time / 1000)
            manager.draw_ui(screen)

        pressed_keys = pygame.key.get_pressed()
        
        if ui_status == "game":
            # update elements
            tiles_rendered = game.update(camera, map, player, rplayers, pressed_keys, screen, cinematic, tick_time, udp_sock, server_ip, id, auth_token)

            # debug
            if (time.time() - debug.time1) >= 1:
                debug.tick(player)
            debug.update(player, screen, myfont, tiles_rendered)

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
    manager = pygame_gui.UIManager((screen_width, screen_height), 'theme.json')
    
    cinematic = False
    screen = pygame.display.set_mode((screen_width, screen_height))

    map = m.Map("map1.json", 80, 60, screen_width, screen_height)
    camera = c.Camera(screen_width, screen_height, map.map_size, map.tile_size)

    rplayers = []

    # connect socket
    id, auth_token, tcp_sock = tcp_socket.connect(server_ip, 12860)
    udp_sock = udp_socket.connect(server_ip, 12861, auth_token)

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

    main_thread(screen, udp_sock, screen_width, screen_height, cinematic, camera, map, fps, id, auth_token, rplayers, server_ip)