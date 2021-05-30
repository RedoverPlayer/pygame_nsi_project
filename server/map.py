import pygame
import json
from pygame.cursors import tri_left

class MapTile(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, x, y, tile_size, type="wall"):
        super(MapTile, self).__init__()
        self.surf = pygame.Surface((tile_size, tile_size))

        self.type = type

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.coords = [x, y]
        self.tile_size = tile_size

        # Rect coords
        self.left = x
        self.right = x + tile_size
        self.top = y
        self.bottom = y + tile_size

        if self.type == "cactus":
            self.left += self.tile_size // 3
            self.right -= self.tile_size // 3
            self.top += self.tile_size // 3
            self.bottom -= self.tile_size // 3

class Map:
    id_to_tile = ["terrain", "wall", "bush", "water", "crate", "barrel", "cactus"]
    tile_to_id = {"terrain": 0, "wall": 1, "bush": 2, "water": 3, "crate": 4, "barrel": 5, "cactus": 6}

    def __init__(self, map_file, tile_size, map_size, screen_width, screen_height):
        # Load map from json
        with open(map_file, "r") as f:
            map_data = json.loads(f.read())
            map_tiles = []

        # generating map tiles
        x_coord = 0
        y_coord = 0

        for y in map_data["tiles"]:
            x_coord = 0
            tmp = []
            for x in y:
                tmp.append(MapTile(screen_width, screen_height, x_coord, y_coord, tile_size, Map.id_to_tile[x]))
                x_coord += tile_size
            map_tiles.append(tmp)
            y_coord += tile_size

        self.tiles = map_tiles
        self.map_size = map_size
        self.tile_size = tile_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spawn_points = map_data["spawn_points"]

    def getTilesAroundCoords(self, coords):
        # adding map tiles to the screen
        coords[0], coords[1] = int(coords[0]), int(coords[1])
        screen_borders = (coords[0] - self.screen_width // 2, coords[1] - self.screen_height // 2)
        tiles_in_viewport = []

        for i in range(self.screen_height // self.tile_size + 2):
            i2 = 0
            left_limit = screen_borders[0] // self.tile_size
            y_tile = screen_borders[1] // 80 + i

            if (left_limit) < 0:
                left_limit = 0
            if y_tile > 59:
                y_tile = 59

            for tile in self.tiles[y_tile][left_limit:screen_borders[0] // self.tile_size + self.screen_width // self.tile_size + 1]:
                tiles_in_viewport.append(tile)
                i2 += 1

        return tiles_in_viewport