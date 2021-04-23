from re import M
import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, username, size=(60, 60)) -> None:
        super().__init__()

        self.surf = pygame.Surface(size)
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.size = size
        self.angle = 0

        self.hp = 400

        self.coords = [0, 0]

        self.size = size

        self.screen_width = screen_width
        self.screen_height = screen_height

        # Other classes
        self.username = Username(username)
        self.hpbar = HPBar((int(self.size[0] * 1.5), self.size[1]), self)

    def mwdt(self, number):
        return (number - self.size[0]) / 2

    def rotate(self, angle):
        self.angle = angle

    def render(self, screen, coords):
        playercoords = (
            self.screen_width/2 + self.coords[0] - coords[0] - self.size[0]/2, 
            self.screen_height/2 + self.coords[1] - coords[1] - self.size[1]/2
        )

        screen.blit(pygame.transform.rotate(self.surf, self.angle), playercoords)

    def renderInfoBar(self, screen, coords):
        self.hpbar.update(self.hp)

        playercoords = (
            self.screen_width/2 + self.coords[0] - coords[0] - self.size[0]/2, 
            self.screen_height/2 + self.coords[1] - coords[1] - self.size[1]/2
        )

        usernamecoords = (
            playercoords[0] - self.mwdt(self.username.width),
            playercoords[1] - self.username.height * 2 - self.hpbar.height
        )

        hpbarx = playercoords[0] - self.mwdt(self.hpbar.width)
        hpbary = playercoords[1] - self.hpbar.height * 2

        hpcount = (
            playercoords[0] - self.mwdt(self.hpbar.pvcount.get_width()) + 2,
            hpbary + 2
        )

        screen.blit(self.username.surf, usernamecoords)
        screen.blit(self.hpbar.surf1, (hpbarx, hpbary))
        screen.blit(pygame.transform.scale(self.hpbar.surf2, (int((self.hpbar.size[0] - 4) * (self.hp / 400)), 8)), (hpbarx + 2, hpbary + 2))
        screen.blit(self.hpbar.pvcount, hpcount)

class Username:
    def __init__(self, username: str):
        self.font = pygame.font.SysFont("freesansbold.ttf", 20)
        self.surf = self.font.render(username, True, (250, 250, 250))
        self.width = self.surf.get_width()
        self.height = self.surf.get_height()

class HPBar:
    def __init__(self, size: tuple, player):
        self.font = pygame.font.SysFont("freesansbold.ttf", 15)
        self.pvcount = self.font.render(str(player.hp), True, (250, 250, 250))

        self.surf1 = pygame.Surface((size[0], 12))
        self.surf1.fill((0, 0, 0))

        self.surf2 = pygame.Surface((size[0] - 4, 8))
        self.surf2.fill((0, 200, 0))

        self.width = self.surf1.get_width()
        self.height = self.surf1.get_height()

        self.size = size

    def update(self, player_hp):
        self.pvcount = self.font.render(str(player_hp), True, (250, 250, 250))