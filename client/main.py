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

def main_thread(screen, fps, ui_status, screen_width, screen_height, rplayers, projs, udp_sock, username, id, auth_token, tcp_sock, server_ip, events, event_lock, rpc):
    main_menu = menus.MainMenu(screen_width, screen_height)
    
    while True:
        if ui_status[0] == "main_menu":
            rpc.update(state="In menus")
            main_menu.run(screen, fps, ui_status, events, event_lock)

        elif ui_status[0] == "searching_game":
            search_menu = menus.SearchMenu(screen_width, screen_height)
            search_menu.run(screen, fps, ui_status, events, event_lock, tcp_sock, rpc)

        elif ui_status[0] == "showdown_game":
            rpc.update(state="In game", details="Showdown")
            showdown_game = game.ShowdownGame(screen_width, screen_height, "map1.json", screen, fps, rplayers, projs, udp_sock, server_ip, id, auth_token, username, tcp_sock)
            showdown_game.run(ui_status, events, event_lock)
            rplayers.clear()
        
        elif ui_status[0] == "end_screen":
            end_screen = menus.EndScreen(screen_width, screen_height)
            end_screen.run(screen, fps, ui_status, events, event_lock, rpc)

        elif ui_status[0] == "quit":
            break

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
    
    screen = pygame.display.set_mode((screen_width, screen_height))

    rplayers = []
    projs = []
    ui_status = ["connecting"]
    events = []
    event_lock = threading.Lock()

    # connect sockets
    data = []
    thread_1 = threading.Thread(target=tcp_socket.connect, args=(server_ip, 12860, data, ui_status, ))
    thread_1.start()

    connection_menu = menus.ConnectionMenu(screen_width, screen_height)
    connection_menu.run(screen, fps, ui_status)

    username, id, auth_token, tcp_sock = data

    udp_sock = udp_socket.connect(server_ip, 12861, auth_token)
    ui_status = ["main_menu"]

    # create and start main threads
    thread_2 = threading.Thread(target=tcp_socket.run, args=(tcp_sock, id, auth_token, rplayers, screen_width, screen_height, events, event_lock))
    thread_3 = threading.Thread(target=udp_socket.run, args=(udp_sock, rplayers, projs, ))

    thread_2.daemon = True
    thread_3.daemon = True

    thread_2.start()
    thread_3.start()

    # connect discord rich presence
    try:
        rpc = rich_presence.RichPresence(825326652124430366)
        rpc.connect()
        rpc.update("In menus", "Ouais le nom du jeu est pas ouf mais en vrai ça passe")
    except:
        pass

    main_thread(screen, fps, ui_status, screen_width, screen_height, rplayers, projs, udp_sock, username, id, auth_token, tcp_sock, server_ip, events, event_lock, rpc)