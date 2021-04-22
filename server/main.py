import threading
import tcp_socket
import udp_socket
import traceback
import pygame
import socket

def tcp_socket_thread(users, game_search, games):
    while True:
        try:
            tcp_socket.run('', 12860, users, game_search, games)
        except Exception as exception:
            print(traceback.format_exc())

def udp_socket_thread(users, games, udp_sock, udp_clients):
    while True:
        try:  
            udp_socket.run('', 12861, users, games, udp_sock, udp_clients)
        except Exception as exception:
            print(traceback.format_exc())

def games_thread(users, games, udp_sock, udp_clients):
    clock = pygame.time.Clock()
    while True:
        try:
            tick_time = clock.tick(60)
            for game in games:
                game.update(users, games, tick_time, udp_sock, udp_clients)
        except:
            print(traceback.format_exc())

if __name__ == "__main__":
    users = {}
    game_search = {"showdown": []}
    games = []

    events = []
    event_lock = threading.Lock()

    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(('', 12861))
    udp_clients = []

    thread_1 = threading.Thread(target=tcp_socket_thread, args=[users, game_search, games])
    thread_2 = threading.Thread(target=udp_socket_thread, args=[users, games, udp_sock, udp_clients])
    thread_3 = threading.Thread(target=games_thread, args=[users, games, udp_sock, udp_clients])

    thread_1.start()
    thread_2.start()
    thread_3.start()