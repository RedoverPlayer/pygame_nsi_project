import pygame
import json

class MapTile(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, x, y, tile_size, type="wall"):
        super(MapTile, self).__init__()
        self.type = type
        self.is_spawn = False
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.coords = [x * tile_size, y * tile_size]
        self.tile_size = tile_size

        # Rect coords
        self.x = x
        self.y = y

        self.changeSize(tile_size)

    def changeSize(self, tile_size):
        self.left = self.x * tile_size
        self.right = self.x * tile_size + tile_size
        self.top = self.y * tile_size
        self.bottom = self.y * tile_size + tile_size

        self.tile_size = tile_size
        self.coords = [self.x * tile_size, self.y * tile_size]

        self.surf = pygame.Surface((tile_size, tile_size))
        self.surf.fill((255, 115, 0) if self.type == "wall" else (0, 140, 255) if self.type == "water" else (255, 255, 0) if self.type == "bush" else (234, 163, 94) if self.type == "crate" else (215, 0, 0) if self.type == "spawn" else (0, 81, 0))
        self.rect = self.surf.get_rect()

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

    def changeType(self, type):
        self.type = type
        self.surf.fill((255, 115, 0) if self.type == "wall" else (0, 140, 255) if self.type == "water" else (255, 255, 0) if self.type == "bush" else (234, 163, 94) if self.type == "crate" else (215, 0, 0) if self.type == "spawn" else (0, 81, 0))
        
        self.changeSize(self.tile_size)

    def update(self, screen, mouse, tool, mouse_buttons, margin_left, spawn_mode):
        if mouse[0] > self.left + margin_left and mouse[0] < self.right + margin_left and mouse[1] > self.top and mouse[1] < self.bottom:
            tmp = self.type
            self.changeType(tool)
            screen.blit(self.surf, (self.coords[0] + margin_left, self.coords[1]))
            
            if tool in ("wall", "crate", "cactus", "barrel"):
                screen.blit(self.surf2, (self.coords[0] + margin_left, self.coords[1] - self.tile_size // 2))

            self.changeType(tmp)

            if mouse_buttons[0]:
                if spawn_mode[0]:
                    self.is_spawn = True
                else:
                    self.changeType(tool)
            elif mouse_buttons[1]:
                return self.type
            elif mouse_buttons[2]:
                if spawn_mode[0]:
                    self.is_spawn = False
                else:
                    self.changeType("terrain")
        else:
            if spawn_mode[0] and self.is_spawn:
                self.surf.fill((215, 0, 0))
                screen.blit(self.surf, (self.coords[0] + margin_left, self.coords[1]))
                self.surf.fill((255, 115, 0) if self.type == "wall" else (0, 140, 255) if self.type == "water" else (255, 255, 0) if self.type == "bush" else (234, 163, 94) if self.type == "crate" else (215, 0, 0) if self.type == "spawn" else (0, 81, 0))
            else:
                screen.blit(self.surf, (self.coords[0] + margin_left, self.coords[1]))
                if self.type in ("wall", "crate", "cactus", "barrel"):
                    screen.blit(self.surf2, (self.coords[0] + margin_left, self.coords[1] - self.tile_size // 2))

class Map:
    id_to_tile = ["terrain", "wall", "bush", "water", "crate", "barrel", "cactus"]
    tile_to_id = {"terrain": 0, "wall": 1, "bush": 2, "water": 3, "crate": 4, "barrel": 5, "cactus": 6}

    def __init__(self, map_file, tile_size, map_size, screen_width, screen_height):
        global map_data

        # Load map from json
        with open(map_file, "r") as f:
            map = json.loads(f.read())
            map_tiles = []

        map_data = map.copy()

        # generating map tiles
        x_coord = 0
        y_coord = 0

        for y in map["tiles"]:
            x_coord = 0
            for x in y:
                map_tiles.append(MapTile(screen_width, screen_height, x_coord, y_coord, tile_size, Map.id_to_tile[x]))
                x_coord += 1
            y_coord += 1

        self.tiles = map_tiles
        self.map_size = map_size
        self.tile_size = tile_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spawn_points = map_data["spawn_points"]

        for spawn_point in map_data["spawn_points"]:
            for tile in self.tiles:
                if tile.x == spawn_point[0] and tile.y == spawn_point[1]:
                    tile.is_spawn = True

    def update(self, screen, mouse, tools, mouse_buttons, margin_left, spawn_mode):
        # adding map tiles to the screen
        tiles_in_viewport = []
        foreground_tiles = []
        for tile in self.tiles:
            if tile.type in ("wall", "crate", "cactus", "barrel"):
                foreground_tiles.append(tile)
            else:
                tiles_in_viewport.append(tile)
        tiles_rendered = [tile.update(screen, mouse, tools, mouse_buttons, margin_left, spawn_mode) for tile in tiles_in_viewport]
        return tiles_rendered + [tile.update(screen, mouse, tools, mouse_buttons, margin_left, spawn_mode) for tile in foreground_tiles]