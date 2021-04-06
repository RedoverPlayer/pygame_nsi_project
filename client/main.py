from socket import socket
import pygame
import json
import time
import threading
import multiprocessing

import player as p
import map_tile
import remote_player
import udp_socket
import camera as c

from pygame.locals import (
    QUIT,
)

def main_thread(udp_sock, screen_width, screen_height, rplayer, map_size, tile_size, cinematic, camera):
    myfont = pygame.font.SysFont("freesansbold.ttf", 48)
    screen = pygame.display.set_mode((screen_width, screen_height))

    screen.fill((50, 50, 50))

    # loading player
    player = p.Player(screen_width, screen_height, (60, 60))

    # loading map tiles
    with open("map1.json", "r") as f:
        map = json.loads(f.read())

    map_tiles = []

    # generating map tiles
    x_coord = 0
    y_coord = 0

    for y in map:
        x_coord = 0
        tmp = []
        for x in y:
            tmp.append(map_tile.MapTile(screen_width, screen_height, x_coord, y_coord, tile_size, x))
            x_coord += tile_size
        map_tiles.append(tmp)
        y_coord += tile_size

    manager = multiprocessing.Manager()

    running = True

    clock = pygame.time.Clock()
    
    # variables for on screen debug
    tmp = player.coords.copy()
    count = 0
    speed = "0"
    fps = 0
    fps_text = "1"
    time1 = time.time()
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos_1 = mouse_pos

    # main loop
    while running:
        # The game runs at max 144 FPS (a little less due to the time of computation of each frame)
        tick_time = clock.tick(144)
        count += tick_time
        fps += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # changing player coords when pressing keys
        pressed_keys = pygame.key.get_pressed()

        # background color
        screen.fill((50, 50, 50))

        # adding map tiles to the screen
        screen_borders = (camera.coords[0] - screen_width // 2, camera.coords[1] - screen_height // 2)
        tiles_in_viewport = []
        for i in range(screen_height // tile_size + 2):
            i2 = 0
            left_limit = screen_borders[0] // tile_size
            if (left_limit) < 0:
                left_limit = 0
            for tile in map_tiles[screen_borders[1] // 80 + i][left_limit:screen_borders[0] // tile_size + screen_width // tile_size + 1]:
                tiles_in_viewport.append(tile)
                i2 += 1

        tiles_rendered = [tile.update(screen, camera.coords) for tile in tiles_in_viewport]

        # update elements
        rplayer.update(screen, camera.coords)
        player.update(pressed_keys, tiles_rendered, map_size, tile_size, tick_time, screen, camera, 2)

        # ensure camera does not go to the border
        if not cinematic:
            camera.update(player.coords, map_size, tile_size)

        # add the player to the screens
        udp_socket.sendCoords(udp_sock, ("localhost", 12861), player.coords)

        # debug
        playercoords = myfont.render(str(player.coords), True, (250, 250, 250))
        screen.blit(playercoords, (5, 5))
        
        tiles_number = myfont.render("Rendered tiles : " + str(len(tiles_rendered)), True, (250, 250, 250))
        screen.blit(tiles_number, (5, 50))

        if count >= 1000:
            speed = str(round(((player.coords[0] - tmp[0])**2 + (player.coords[1] - tmp[1])**2)**0.5, 2))
            tmp = player.coords.copy()
            count = 0

        if (time.time() - time1) >= 1:
            fps_text = str(int(fps // (time.time() - time1)))
            fps = 0
            time1 = time.time()

        player_speed = myfont.render("Speed : " + speed, True, (250, 250, 250))
        screen.blit(player_speed, (5, 100))

        fps_display = myfont.render(fps_text + " FPS", True, (250, 250, 250))
        screen.blit(fps_display, (5, 150))

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

def render_tiles(tiles_rendered, map_tiles, queue, camera_coords):
    screen = queue.get()
    tiles_rendered += [elem for elem in [map_tile.update(screen, camera_coords) for map_tile in map_tiles] if elem != None]

if __name__ == "__main__":
    # initialize pygame
    pygame.init()
    pygame.font.init()

    # window title
    pygame.display.set_caption("NSI project")

    # ---- config ----
    screen_width = 1920
    screen_height = 1080

    map_size = 60
    tile_size = 80
    # -----------------

    cinematic = False

    remoteplayer = remote_player.RemotePlayer(screen_width, screen_height)
    camera = c.Camera(screen_width, screen_height, map_size, tile_size)

    # connect socket
    udp_sock = udp_socket.connect("localhost", 12861)

    # data_lock = threading.Lock()
    thread_1 = threading.Thread(target=main_thread, args=(udp_sock, screen_width, screen_height, remoteplayer, map_size, tile_size, cinematic, camera, ))
    thread_2 = threading.Thread(target=socket_receive, args=(udp_sock, remoteplayer, ))
    # thread_3 = threading.Thread(target=c.move_camera_to, args=((camera.width // 2 - tile_size, camera.height // 2 - tile_size), map_size, tile_size, cinematic, camera, ))

    thread_1.start()
    thread_2.start()

    time.sleep(1)
    # thread_3.start()