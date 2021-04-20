import threading
import tcp_socket
import udp_socket
import traceback
import pygame

def tcp_socket_thread(users, game_search, games):
    while True:
        try:
            tcp_socket.run('', 12860, users, game_search, games)
        except Exception as exception:
            print(traceback.format_exc())

def udp_socket_thread(users, games):
    while True:
        try:  
            udp_socket.run('', 12861, users, games)
        except Exception as exception:
            print(traceback.format_exc())

def games_thread(users, games):
    clock = pygame.time.Clock()
    while True:
        try:
            clock.tick(60)
            for game in games:
                game.update(users, games)
        except:
            print(traceback.format_exc())

if __name__ == "__main__":
    users = {}
    game_search = {"showdown": []}
    games = []

    events = []
    event_lock = threading.Lock()

    thread_1 = threading.Thread(target=tcp_socket_thread, args=[users, game_search, games])
    thread_2 = threading.Thread(target=udp_socket_thread, args=[users, games])
    thread_3 = threading.Thread(target=games_thread, args=[users, games])

    thread_1.start()
    thread_2.start()
    thread_3.start()