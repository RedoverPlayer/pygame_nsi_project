import pygame
import abilities

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width: int, screen_height: int, size: tuple=(60, 60)):
        super(Player, self).__init__()
        self.surf = pygame.Surface(size)
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.size = size
        self.angle = 0
        
        # Other classes
        self.username = Username("Test Player")
        self.hpbar = HPBar((int(self.size[0] * 1.5), self.size[1]))

        self.coords = [0, 0]

        self.size = size

        self.screen_width = screen_width
        self.screen_height = screen_height

    def rotate(self, angle):
        self.angle = angle

    def update(self, pressed_keys, rendered_tiles, map_size, tile_size, tick_time, screen, camera, speed=2):
        movement_speed = tick_time // 4

        left = self.coords[0] - self.size[0] // 2
        right = self.coords[0] + self.size[0] // 2
        top = self.coords[1] - self.size[1] // 2
        bottom = self.coords[1] + self.size[1] // 2

        if pressed_keys[pygame.K_q]:
            if self.coords[0] - movement_speed > self.size[0] // 2:
                moved = False
                for tile in rendered_tiles:
                    # check if the left side of the player collides with the right side of the tile
                    if (tile.type == "wall" or tile.type == "cactus" or tile.type == "barrel" or tile.type == "box") and (bottom > tile.top) and (top < tile.bottom) and (left >= tile.right) and (left - movement_speed < tile.right):
                        self.coords[0] += tile.right - left
                        moved = True
                        break
                if not moved:
                    self.coords[0] -= movement_speed
            else:
                self.coords[0] -= self.coords[0] - self.size[0] // 2
                    
        if pressed_keys[pygame.K_d]:
            if self.coords[0] + movement_speed < map_size * tile_size - self.size[0] // 2:
                moved = False
                for tile in rendered_tiles:
                    # check if the right side of the player collides with the left side of the tile
                    if (tile.type == "wall" or tile.type == "cactus" or tile.type == "barrel" or tile.type == "box") and (bottom > tile.top) and (top < tile.bottom) and (right <= tile.left) and (right + movement_speed > tile.left):
                        self.coords[0] += tile.left - right
                        moved = True
                        break
                if not moved:
                    self.coords[0] += movement_speed
            else:
                self.coords[0] -= self.coords[0] - (map_size * tile_size - self.size[0] // 2)

        if pressed_keys[pygame.K_z]:
            if self.coords[1] - movement_speed > self.size[1] // 2:
                moved = False
                for tile in rendered_tiles:
                    # check if the top of the player collides with the bottom of the tile
                    if (tile.type == "wall" or tile.type == "cactus" or tile.type == "barrel" or tile.type == "box") and (right > tile.left) and (left < tile.right) and (top >= tile.bottom) and (top - movement_speed < tile.bottom):
                        self.coords[1] += tile.bottom - top
                        moved = True
                        break
                if not moved:
                    self.coords[1] -= movement_speed
            else:
                self.coords[1] -= self.coords[1] - self.size[1] // 2

        if pressed_keys[pygame.K_s]:
            if self.coords[1] + movement_speed < map_size * tile_size - self.size[1] // 2:
                moved = False
                for tile in rendered_tiles:
                    # check if the bottom of the player collides with the top of the tile
                    if (tile.type == "wall" or tile.type == "cactus" or tile.type == "barrel" or tile.type == "box") and (right > tile.left) and (left < tile.right) and (bottom <= tile.top) and (bottom + movement_speed > tile.top):
                        self.coords[1] += tile.top - bottom
                        moved = True
                        break
                if not moved:
                    self.coords[1] += movement_speed
            else:
                self.coords[1] -= self.coords[1] - (map_size * tile_size - self.size[1] // 2)
        
        if pressed_keys[pygame.K_SPACE]:
            proj1= abilities.Projectile(self.screen_width, self.screen_height, self.coords)

        screen.blit(pygame.transform.rotate(self.surf, self.angle), (self.screen_width/2 + self.coords[0] - camera.coords[0] - self.size[0]/2, self.screen_height/2 + self.coords[1] - camera.coords[1] - self.size[1]/2))
        screen.blit(self.username.surf,
        (
            self.screen_width/2 + self.coords[0] - camera.coords[0] - self.size[0]/2 - (self.username.width - self.size[0]) // 2,
            self.screen_height/2 + self.coords[1] - camera.coords[1] - self.size[1]/2 - self.username.height * 2 - self.hpbar.height)
        )
        screen.blit(self.hpbar.surf1,
        (
            self.screen_width/2 + self.coords[0] - camera.coords[0] - self.size[0]/2 - (self.hpbar.width - self.size[0]) // 2,
            self.screen_height/2 + self.coords[1] - camera.coords[1] - self.size[1]/2 - self.hpbar.height * 2)
        )
        screen.blit(self.hpbar.surf2,
        (
            self.screen_width/2 + self.coords[0] - camera.coords[0] - self.size[0]/2 - (self.hpbar.width - self.size[0]) // 2 + 2,
            self.screen_height/2 + self.coords[1] - camera.coords[1] - self.size[1]/2 - self.hpbar.height * 2 + 2)
        )
        screen.blit(self.hpbar.pvcount,
        (
            self.screen_width/2 + self.coords[0] - camera.coords[0] - self.size[0]/2 - (self.hpbar.pvcount.get_width() - self.size[0]) // 2 + 2,
            self.screen_height/2 + self.coords[1] - camera.coords[1] - self.size[1]/2 - self.hpbar.height * 2 + 2)
        )

class Username:
    def __init__(self, username: str):
        self.font = pygame.font.SysFont("freesansbold.ttf", 20)
        self.surf = self.font.render(username, True, (250, 250, 250))
        self.width = self.surf.get_width()
        self.height = self.surf.get_height()

class HPBar:
    def __init__(self, size: tuple):
        self.font = pygame.font.SysFont("freesansbold.ttf", 15)
        self.pvcount = self.font.render("400", True, (250, 250, 250))

        self.surf1 = pygame.Surface((size[0], 12))
        self.surf1.fill((0, 0, 0))

        self.surf2 = pygame.Surface((size[0] - 4, 8))
        self.surf2.fill((0, 200, 0))

        self.width = self.surf1.get_width()
        self.height = self.surf1.get_height()

class Sight:
    def __init__(self):
        self.surf = pygame.Surface((5, 5))
    
    def rotate(self, angle: float):
        # fonction maths compliquée
        self.surf.rotate(angle)