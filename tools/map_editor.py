import json
import pygame
from pygame import mouse

from pygame.locals import (MOUSEWHEEL, QUIT)

# INFO
# To use the map editor, place tha map (named map1.json) into the tools folder and start this program. To add a tile, click left, to remove a tile (place terrain) click right.
# To pick the type of the tile the mouse cursor is in, click on the mouse wheel. To change tool, scroll.

# ---- Config ----

window_size = (1080, 1080) # The map display will be a square. Note that the window should be divisible by 60 to fit the size of the map
frames_per_second = 144

# ----------------

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

    def changeType(self, type):
        self.type = type
        self.surf.fill((255, 115, 0) if self.type == "wall" else (0, 140, 255) if self.type == "water" else (255, 255, 0) if self.type == "bush" else (234, 163, 94) if self.type == "crate" else (0, 81, 0))
        
        if self.type == "wall":
            self.surf2 = pygame.image.load("img/wall.png")
            self.surf2 = pygame.transform.scale(self.surf2, (self.tile_size, self.tile_size + self.tile_size // 2))
        elif self.type == "crate":
            self.surf2 = pygame.image.load("img/crate.png")
            self.surf2 = pygame.transform.scale(self.surf2, (self.tile_size, self.tile_size + self.tile_size // 2))
        elif self.type == "barrel":
            self.surf2 = pygame.image.load("img/barrel.png")
            self.surf2 = pygame.transform.scale(self.surf2, (self.tile_size, self.tile_size + self.tile_size // 2))
            self.surf2.set_colorkey((255, 255, 255))
        elif self.type == "cactus":
            self.surf2 = pygame.image.load("img/cactus.png")
            self.surf2 = pygame.transform.scale(self.surf2, (self.tile_size, self.tile_size + self.tile_size // 2))
            self.surf2.set_colorkey((255, 255, 255))

    def update(self, screen, mouse, tool, mouse_buttons):
        if mouse[0] > self.left and mouse[0] < self.right and mouse[1] > self.top and mouse[1] < self.bottom:
            tmp = self.type
            self.changeType(tool)
            screen.blit(self.surf, (self.coords[0], self.coords[1]))
            
            if tool in ("wall", "crate", "cactus", "barrel"):
                screen.blit(self.surf2, (self.coords[0], self.coords[1] - self.tile_size // 2))

            self.changeType(tmp)

            if mouse_buttons[0]:
                self.changeType(tool)
            elif mouse_buttons[1]:
                return self.type
            elif mouse_buttons[2]:
                self.changeType("terrain")
        else:
            screen.blit(self.surf, (self.coords[0], self.coords[1]))
            if self.type in ("wall", "crate", "cactus", "barrel"):
                screen.blit(self.surf2, (self.coords[0], self.coords[1] - self.tile_size // 2))

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
            for x in y:
                map_tiles.append(MapTile(screen_width, screen_height, x_coord, y_coord, tile_size, x))
                x_coord += tile_size
            y_coord += tile_size

        self.tiles = map_tiles
        self.map_size = map_size
        self.tile_size = tile_size
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, screen, mouse, tools, mouse_buttons):
        # adding map tiles to the screen
        tiles_in_viewport = []
        foreground_tiles = []
        for tile in self.tiles:
            if tile.type in ("wall", "crate", "cactus", "barrel"):
                foreground_tiles.append(tile)
            else:
                tiles_in_viewport.append(tile)
        tiles_rendered = [tile.update(screen, mouse, tools, mouse_buttons) for tile in tiles_in_viewport]
        return tiles_rendered + [tile.update(screen, mouse, tools, mouse_buttons) for tile in foreground_tiles]

SCREEN_WIDTH = window_size[0]
SCREEN_HEIGHT = window_size[1]

pygame.init()
pygame.font.init()

# window title
pygame.display.set_caption("NSI project - Map Editor")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((50, 50, 50))

# loading map
map = Map("map1.json", min(window_size) // 60, 60, SCREEN_WIDTH, SCREEN_HEIGHT)

running = True

clock = pygame.time.Clock()

tools = ["wall", "water", "bush", "cactus", "barrel", "crate"]
tool = 0

# main loop
while running:
    # The game runs at max 144 FPS (a little less due to the time of computation of each frame)
    tick_time = clock.tick(frames_per_second)

    mouse_button_pos = None
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEWHEEL:
            if event.y == -1:
                if tool == 0:
                    tool = len(tools) - 1
                else:
                    tool -= 1
            elif event.y == 1:
                if tool == len(tools) - 1:
                    tool = 0
                else:
                    tool += 1
                    
    # changing player coords when pressing keys
    pressed_keys = pygame.key.get_pressed()

    # background color
    screen.fill((50, 50, 50))

    # adding map tiles to the screen
    tiles_rendered = [elem for elem in map.update(screen, pygame.mouse.get_pos(), tools[tool], pygame.mouse.get_pressed()) if elem != None]
    if len(tiles_rendered) > 0:
        if tiles_rendered[0] != "terrain":
            tool = tools.index(tiles_rendered[0])

    # render elements to the screen
    pygame.display.flip()

map_list = [["terrain" for _ in range(60)] for _ in range(60)]
x = 0
y = 0
for tile in map.tiles:
    map_list[y][x] = tile.type
    x += 1
    if x > 59:
        x = 0
        y += 1
    if y >= 60:
        break

with open("map1.json", "w") as f:
    f.write(json.dumps(map_list))