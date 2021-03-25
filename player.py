import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 75))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

        self.coords = [0, 0]

        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, pressed_keys, rendered_tiles, map_size, tile_size, tick_time, speed=2):
        movement_speed = 2 * tick_time / 8
        if pressed_keys[pygame.K_q]:
            if self.coords[0] - movement_speed > 38:
                self.coords[0] -= movement_speed
            else:
                self.coords[0] -= self.coords[0] - 38
        if pressed_keys[pygame.K_d]:
            if self.coords[0] + movement_speed < map_size * tile_size - 38:
                self.coords[0] += movement_speed
            else:
                self.coords[0] -= self.coords[0] - (map_size * tile_size - 38)
        if pressed_keys[pygame.K_z]:
            if self.coords[1] - movement_speed > 38:
                self.coords[1] -= movement_speed
            else:
                self.coords[1] -= self.coords[1] - 38
        if pressed_keys[pygame.K_s]:
            if self.coords[1] + movement_speed < map_size * tile_size - 38:
                self.coords[1] += movement_speed
            else:
                self.coords[1] -= self.coords[1] - (map_size * tile_size - 38)