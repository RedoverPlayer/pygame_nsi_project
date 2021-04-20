import pygame
import math 
import time

class Projectile(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, coords, size=(12, 12)):
        super(Projectile, self).__init__()
        self.surf = pygame.Surface(size)
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.size = size
        self.coords = coords
        self.screen_width = screen_width
        self.sreen_height = screen_height
        
        mouse_coord = pygame.mouse.get_pos()
        x , y = mouse_coord[0] - screen_width//2, mouse_coord[1] - screen_height//2
        norme = math.sqrt((mouse_coord[0]-coords[0])**2+(mouse_coord[1]-coords[1])**2)
        if y!=0:
            truc = -math.atan2(y, x)
            print (truc)



    def update(self, screen, player_coords):
        left = self.coords[0] - self.size[0] // 2
        right = self.coords[0] + self.size[0] // 2
        top = self.coords[1] - self.size[1] // 2
        bottom = self.coords[1] + self.size[1] // 2

        if ((self.coords[0] - player_coords[0]) + self.screen_width / 2) > -1 * self.size[0] and ((self.coords[0] - player_coords[0]) + self.screen_width / 2) < self.screen_width and (-1 * player_coords[1] + self.coords[1]) + self.screen_height / 2 > -1 * self.size[1] and (-1 * player_coords[1] + self.coords[1]) + self.screen_height / 2 < self.screen_height + self.size[1]:
            screen.blit(self.surf, ((self.coords[0] - player_coords[0]) + self.screen_width // 2 - self.size[0] // 2, (-1*player_coords[1] + self.coords[1]) + self.screen_height // 2 - self.size[1] // 2))