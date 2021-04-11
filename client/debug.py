import time

class Debug:
    def __init__(self, player):
        self.coords_1 = player.coords.copy()
        self.speed = "0"
        self.fps = 0
        self.fps_text = "1"
        self.time1 = time.time()
    
    def tick(self, player):
        self.speed = str(int(((player.coords[0] - self.coords_1[0])**2 + (player.coords[1] - self.coords_1[1])**2)**0.5))
        self.fps_text = str(int(self.fps // (time.time() - self.time1)))

        self.coords_1 = player.coords.copy()
        self.fps = 0
        self.time1 = time.time()

    def update(self, player, screen, myfont, tiles_rendered):
        playercoords = myfont.render(str(player.coords), True, (250, 250, 250))
        screen.blit(playercoords, (5, 5))
        
        tiles_number = myfont.render("Rendered tiles : " + str(len(tiles_rendered)), True, (250, 250, 250))
        screen.blit(tiles_number, (5, 50))

        player_speed = myfont.render("Speed : " + self.speed, True, (250, 250, 250))
        screen.blit(player_speed, (5, 100))

        fps_display = myfont.render(self.fps_text + " FPS", True, (250, 250, 250))
        screen.blit(fps_display, (5, 150))