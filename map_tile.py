import pygame
from pygame.cursors import tri_left

class MapTile(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, x, y, tile_size, type="wall"):
        print(x, y)
        super(MapTile, self).__init__()
        self.surf = pygame.Surface((tile_size, tile_size))
        self.surf.fill((255, 115, 0) if type == "wall" else (0, 140, 255) if type == "water" else (0, 81, 0))
        self.rect = self.surf.get_rect()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.coords = [x, y]
        self.type = type
        self.tile_size = tile_size

        # Rect coords
        self.top_left = (x, y)
        self.top_right = (x + tile_size, y)

        self.bottom_right = (x + tile_size, y + tile_size)
        self.bottom_left = (x, y + tile_size)

    def update(self, screen, player_coords):
        # add the tile to the screen the tile if its coordinates are on the window
        if ((self.coords[0] - player_coords[0]) + self.screen_width / 2) > -1 * self.tile_size and ((self.coords[0] - player_coords[0]) + self.screen_width / 2) < self.screen_width and (-1 * player_coords[1] - self.coords[1]) + self.screen_height / 2 > -1 * self.tile_size and (-1 * player_coords[1] - self.coords[1]) + self.screen_height / 2 < self.screen_height + self.tile_size:
            screen.blit(self.surf, ((self.coords[0] - player_coords[0]) + self.screen_width / 2, (-1 * player_coords[1] - self.coords[1]) + self.screen_height / 2))
            return self
        else:
            return None