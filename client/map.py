import pygame
import json
from pygame.cursors import tri_left

class MapTile(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, x, y, tile_size, type="wall"):
        super(MapTile, self).__init__()
        self.surf = pygame.Surface((tile_size, tile_size))
        
        self.type = type
        self.surf.fill((255, 115, 0) if self.type == "wall" else (0, 140, 255) if self.type == "water" else (255, 255, 0) if self.type == "bush" else (234, 163, 94) if self.type == "crate" else (0, 81, 0))
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

        if self.type == "wall":
            self.surf2 = pygame.image.load("img/wall.png")
            self.surf2 = pygame.transform.scale(self.surf2, (tile_size, tile_size + tile_size // 2))
        elif self.type == "crate":
            self.surf2 = pygame.image.load("img/crate.png")
            self.surf2 = pygame.transform.scale(self.surf2, (tile_size, tile_size + tile_size // 2))
        elif self.type == "barrel":
            self.surf2 = pygame.image.load("img/barrel.png")
            self.surf2 = pygame.transform.scale(self.surf2, (tile_size, tile_size + tile_size // 2))
            self.surf2.set_colorkey((255, 255, 255))
        elif self.type == "cactus":
            self.surf2 = pygame.image.load("img/cactus.png")
            self.surf2 = pygame.transform.scale(self.surf2, (tile_size, tile_size + tile_size // 2))
            self.surf2.set_colorkey((255, 255, 255))
            
            self.left += self.tile_size // 3
            self.right -= self.tile_size // 3
            self.top += self.tile_size // 3
            self.bottom -= self.tile_size // 3

    def update(self, screen, coords, no_render=False):
        if self.type in ("wall", "crate", "cactus", "barrel"):
            if not no_render:
                screen.blit(self.surf2, ((self.coords[0] - coords[0]) + self.screen_width / 2, (-1*coords[1] + self.coords[1]) + self.screen_height / 2 - self.tile_size // 2))
            else:
                screen.blit(self.surf, ((self.coords[0] - coords[0]) + self.screen_width / 2, (-1*coords[1] + self.coords[1]) + self.screen_height / 2))
        else:
            screen.blit(self.surf, ((self.coords[0] - coords[0]) + self.screen_width / 2, (-1*coords[1] + self.coords[1]) + self.screen_height / 2))
        return self

class Map:
    def __init__(self, map_file, tile_size, map_size, screen_width, screen_height):
        # Load map from json
        with open(map_file, "r") as f:
            map = json.loads(f.read())
            map_tiles = []

        # generating map tiles
        x_coord = 0
        y_coord = 0

        for y in map:
            x_coord = 0
            tmp = []
            for x in y:
                tmp.append(MapTile(screen_width, screen_height, x_coord, y_coord, tile_size, x))
                x_coord += tile_size
            map_tiles.append(tmp)
            y_coord += tile_size

        self.tiles = map_tiles
        self.map_size = map_size
        self.tile_size = tile_size
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, coords, screen, player):
        # adding map tiles to the screen
        coords[0], coords[1] = int(coords[0]), int(coords[1])
        screen_borders = (coords[0] - self.screen_width // 2, coords[1] - self.screen_height // 2)
        tiles_in_viewport = []
        foreground_tiles = []

        for i in range(self.screen_height // self.tile_size + 2):
            i2 = 0
            left_limit = screen_borders[0] // self.tile_size
            y_tile = screen_borders[1] // 80 + i

            if (left_limit) < 0:
                left_limit = 0
            if y_tile > 59:
                y_tile = 59

            for tile in self.tiles[y_tile][left_limit:screen_borders[0] // self.tile_size + self.screen_width // self.tile_size + 1]:
                if tile.type in ("wall", "crate", "cactus", "barrel"):
                    foreground_tiles.append(tile)
                    tiles_in_viewport.append(tile)
                else:
                    tiles_in_viewport.append(tile)
                i2 += 1

        return [tile.update(screen, coords, True) for tile in tiles_in_viewport], foreground_tiles