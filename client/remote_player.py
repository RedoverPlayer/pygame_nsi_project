import pygame

class RemotePlayer(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, size=(60, 60)):
        super(RemotePlayer, self).__init__()
        self.surf = pygame.Surface(size)
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.size = size

        self.coords = [0, 0]

        self.username = Username("Remote player")

        self.size = size

        self.top_left = (-size[0] // 2, size[0] // 2)
        self.top_right = (size[0] // 2, size[0] // 2)

        self.bottom_left = (-size[0] // 2, -size[0] // 2)
        self.bottom_right = (size[0] // 2, -size[0] // 2)

        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, screen, coords):
        left = self.coords[0] - self.size[0] // 2
        right = self.coords[0] + self.size[0] // 2
        top = self.coords[1] - self.size[1] // 2
        bottom = self.coords[1] + self.size[1] // 2

        if ((self.coords[0] - coords[0]) + self.screen_width / 2) > -1 * self.size[0] and ((self.coords[0] - coords[0]) + self.screen_width / 2) < self.screen_width and (-1 * coords[1] + self.coords[1]) + self.screen_height / 2 > -1 * self.size[1] and (-1 * coords[1] + self.coords[1]) + self.screen_height / 2 < self.screen_height + self.size[1]:
            screen.blit(self.surf, ((self.coords[0] - coords[0]) + self.screen_width // 2 - self.size[0] // 2, (-1*coords[1] + self.coords[1]) + self.screen_height // 2 - self.size[1] // 2))
            screen.blit(self.username.surf,
            (
                self.screen_width/2 + self.coords[0] - coords[0] - self.size[0]/2 - (self.username.width - self.size[0]) // 2,
                self.screen_height/2 + self.coords[1] - coords[1] - self.size[1]/2 - self.username.height * 2)
            )

class Username:
    def __init__(self, username):
        self.font = pygame.font.SysFont("freesansbold.ttf", 20)
        self.surf = self.font.render(username, True, (250, 250, 250))
        self.width = self.surf.get_width()
        self.height = self.surf.get_height()