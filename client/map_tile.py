import pygame
from pygame.cursors import tri_left

class MapTile(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, x, y, tile_size, type="wall"):
        super(MapTile, self).__init__()
        self.surf = pygame.Surface((tile_size, tile_size))
        self.type = type
        self.surf.fill((255, 115, 0) if self.type == "wall" else (0, 140, 255) if self.type == "water" else (255, 255, 0) if self.type == "bush" else (65, 191, 98) if self.type == "cactus" else (204, 121, 63) if self.type == "barrel" else (234, 163, 94) if self.type == "box" else (0, 81, 0))
        self.rect = self.surf.get_rect()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.coords = [x, y]
        self.tile_size = tile_size

        # Rect coords
        self.left = x
        self.right = x + tile_size
        self.top = y
        self.bottom = y + tile_size

    def update(self, screen, coords):
        # add the tile to the screen if its coordinates are on the window
        # if ((self.coords[0] - coords[0]) + self.screen_width / 2) > -1 * self.tile_size and ((self.coords[0] - coords[0]) + self.screen_width / 2) < self.screen_width and (-1 * coords[1] + self.coords[1]) + self.screen_height / 2 > -1 * self.tile_size and (-1 * coords[1] + self.coords[1]) + self.screen_height / 2 < self.screen_height + self.tile_size:
        screen.blit(self.surf, ((self.coords[0] - coords[0]) + self.screen_width / 2, (-1*coords[1] + self.coords[1]) + self.screen_height / 2))
        return self
        # else:
        #     return None