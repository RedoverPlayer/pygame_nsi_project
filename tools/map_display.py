import json
import pygame

from pygame.locals import QUIT

# ---- Config ----

window_size = (1200, 1200) # The map display will be a square. Note that the window should be divisible by 60 to fit the size of the map
frames_per_second = 144

# ----------------

class MapTile(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, x, y, tile_size, type="wall"):
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
        self.left = x
        self.right = x + tile_size
        self.top = y
        self.bottom = y + tile_size

    def update(self, screen):
        # add the tile to the screen if its coordinates are on the window
        screen.blit(self.surf, (self.coords[0], self.coords[1]))
        return self

SCREEN_WIDTH = window_size[0]
SCREEN_HEIGHT = window_size[1]

pygame.init()
pygame.font.init()

# window title
pygame.display.set_caption("NSI project - Map Editor")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((50, 50, 50))

# loading map tiles
with open("map1.json", "r") as f:
    map = json.loads(f.read())

map_size = 60
tile_size = min(window_size) // map_size
map_tiles = []

# generating map tiles
x_coord = 0
y_coord = 0

for y in map:
    x_coord = 0
    for x in y:
        map_tiles.append(MapTile(SCREEN_WIDTH, SCREEN_HEIGHT, x_coord, y_coord, tile_size, x))
        x_coord += tile_size
    y_coord += tile_size

running = True

clock = pygame.time.Clock()

# main loop
while running:
    # The game runs at max 144 FPS (a little less due to the time of computation of each frame)
    tick_time = clock.tick(frames_per_second)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # changing player coords when pressing keys
    pressed_keys = pygame.key.get_pressed()

    # background color
    screen.fill((50, 50, 50))

    # adding map tiles to the screen
    tiles_rendered = [elem for elem in [map_tile.update(screen) for map_tile in map_tiles] if elem != None]

    # render elements to the screen
    pygame.display.flip()