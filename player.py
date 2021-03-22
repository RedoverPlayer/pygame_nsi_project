import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 75))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, pressed_keys, speed=1):
        if pressed_keys[pygame.K_z]:
            self.rect.move_ip(0, -1 * speed)
        if pressed_keys[pygame.K_s]:
            self.rect.move_ip(0, speed)
        if pressed_keys[pygame.K_q]:
            self.rect.move_ip(-1 * speed, 0)
        if pressed_keys[pygame.K_d]:
            self.rect.move_ip(speed, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.screen_height:
            self.rect.bottom = self.screen_height