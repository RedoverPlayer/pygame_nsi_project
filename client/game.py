import pygame
import time

import udp_socket
import menus
import map
import camera
import player
import debug as d

class Game:
    def __init__(self, screen_width, screen_height, map_name, screen, fps, rplayers, udp_sock, server_ip, id, auth_token, username):
        self.clock = pygame.time.Clock()

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.cinematic = [False]
        self.fps = fps
        self.font = pygame.font.SysFont("freesansbold.ttf", 48)
        self.player = player.Player(self.screen_width, self.screen_height, username, (60, 60))
        self.running = True

        self.rplayers = rplayers
        self.udp_sock = udp_sock
        self.server_ip = server_ip
        self.id = id
        self.auth_token = auth_token

        self.screen = screen
        self.screen.fill((50, 50, 50))
        self.map = map.Map(map_name, 80, 60, screen_width, screen_height)
        self.camera = camera.Camera(screen_width, screen_height, self.map.map_size, self.map.tile_size)

        self.debug = d.Debug(self.player)

    def update(self):
        tiles_rendered, foreground_tiles = self.map.update(self.camera.coords, self.screen, self.player)

        for rplayer in self.rplayers:
            rplayer.update(self.screen, self.camera.coords)

        self.player.update(self.pressed_keys, tiles_rendered, self.map.map_size, self.map.tile_size, self.tick_time, self.screen, self.camera)

        for tile in foreground_tiles:
            tile.update(self.screen, self.camera.coords)
        
        for rplayer in self.rplayers:
            rplayer.renderInfoBar(self.screen, self.camera.coords)

        self.player.renderInfoBar(self.screen, self.camera.coords)

        # ensure camera does not go to the border
        if not self.cinematic[0]:
            self.camera.update(self.player.coords, self.map.map_size, self.map.tile_size)

        # add the player to the screens
        udp_socket.sendCoords(self.udp_sock, (self.server_ip, 12861), self.player.coords, self.id, self.auth_token)

        return tiles_rendered

    def updateDebug(self, tiles_rendered):
        self.debug.fps += 1
        if (time.time() - self.debug.time1) >= 1:
            self.debug.tick(self.player)
        self.debug.update(self.player, self.screen, self.font, tiles_rendered)

class ShowdownGame(Game):
    def __init__(self, screen_width, screen_height, map_name, screen, fps, rplayers, udp_sock, server_ip, id, auth_token, username):
        Game.__init__(self, screen_width, screen_height, map_name, screen, fps, rplayers, udp_sock, server_ip, id, auth_token, username)
 
    def run(self, ui_status, events, event_lock):
        # main loop
        while self.running:
            self.tick_time = self.clock.tick(self.fps)

            self.screen.fill((50, 50, 50))

            event_lock.acquire()
            for event in events:
                if event["type"] == "game_ended":
                    ui_status[0] = "end_screen"
                    self.running = False
            event_lock.release()

            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    self.running = False
                    ui_status[0] = "quit"

            self.pressed_keys = pygame.key.get_pressed()
            tiles_rendered = self.update()
            self.updateDebug(tiles_rendered)

            # render elements to the screen
            pygame.display.flip()