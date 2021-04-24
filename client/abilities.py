import pygame
import math 
import time

class Projectile(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, player_coords, angle, id, size=(12, 4)):
        super(Projectile, self).__init__()
        self.surf = pygame.image.load("img/projectile_1.png")
        self.surf = pygame.transform.scale(self.surf, (size[0], size[1]))

        self.rect = self.surf.get_rect()
        self.size = size
        self.coords = player_coords.copy()
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.id = id

        self.angle = angle
        self.angle_deg = angle * 180 / math.pi

    def setCoords(self, coords):
        self.coords = coords

    def update(self, screen, camera_coords):
        if ((self.coords[0] - camera_coords[0]) + self.screen_width / 2) > -1 * self.size[0] and ((self.coords[0] - camera_coords[0]) + self.screen_width / 2) < self.screen_width and (-1 * camera_coords[1] + self.coords[1]) + self.screen_height / 2 > -1 * self.size[1] and (-1 * camera_coords[1] + self.coords[1]) + self.screen_height / 2 < self.screen_height + self.size[1]:
            proj_coords = (
                self.screen_width/2 + self.coords[0] - camera_coords[0] - self.size[0]/2, 
                self.screen_height/2 + self.coords[1] - camera_coords[1] - self.size[1]/2
            )

            screen.blit(pygame.transform.rotate(self.surf,  - 1 * self.angle_deg), proj_coords)

def sendProjToServer(screen_width, screen_height, tcp_sock, player_coords, camera_coords):
    mouse_coords = pygame.mouse.get_pos()
    mouse_coords_in_map = (mouse_coords[0] + camera_coords[0] - screen_width // 2, mouse_coords[1] + camera_coords[1] - screen_height // 2)
    player_mouse_vector = (mouse_coords_in_map[0] - player_coords[0], mouse_coords_in_map[1] - player_coords[1])

    forward_vector = (100, 0)

    angle = (math.atan2(player_mouse_vector[1], player_mouse_vector[0]) - math.atan2(forward_vector[1], forward_vector[0]))

    tcp_sock.send(('{"type": "proj", "angle": ' + str(angle) + '}$').encode("ascii"))