import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, size=(60, 60)):
        super(Player, self).__init__()
        self.surf = pygame.Surface(size)
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.size = size

        self.coords = [0, 0]

        self.size = size

        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, pressed_keys, rendered_tiles, map_size, tile_size, tick_time, speed=2):
        movement_speed = 2 * tick_time // 8

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
                        self.coords[0] -= tile.right - left
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