from character import Character
import pygame
import abilities

class Player(Character):
    def __init__(self, screen_width, screen_height, username="Unnamed player", size=(60, 60)) -> None:
        Character.__init__(self, screen_width, screen_height, username, size)

    def update(self, pressed_keys, rendered_tiles, map_size, tile_size, tick_time, screen, camera, projs, tcp_sock, speed=2):
        movement_speed = tick_time / 4

        left = self.coords[0] - self.size[0] / 2
        right = self.coords[0] + self.size[0] / 2
        top = self.coords[1] - self.size[1] / 2
        bottom = self.coords[1] + self.size[1] / 2

        tmpcoords = self.coords

        if pressed_keys[pygame.K_q]:
            if tmpcoords[0] - movement_speed > self.size[0] / 2:
                moved = False
                for tile in rendered_tiles:
                    # check if the left side of the player collides with the right side of the tile
                    if (tile.type == "wall" or tile.type == "cactus" or tile.type == "barrel" or tile.type == "crate") and (bottom > tile.top) and (top < tile.bottom) and (left >= tile.right) and (left - movement_speed < tile.right):
                        tmpcoords[0] += tile.right - left
                        moved = True
                        break
                if not moved:
                    tmpcoords[0] -= movement_speed
            else:
                tmpcoords[0] -= tmpcoords[0] - self.size[0] / 2
                    
        if pressed_keys[pygame.K_d]:
            if tmpcoords[0] + movement_speed < map_size * tile_size - self.size[0] / 2:
                moved = False
                for tile in rendered_tiles:
                    # check if the right side of the player collides with the left side of the tile
                    if (tile.type == "wall" or tile.type == "cactus" or tile.type == "barrel" or tile.type == "crate") and (bottom > tile.top) and (top < tile.bottom) and (right <= tile.left) and (right + movement_speed > tile.left):
                        tmpcoords[0] += tile.left - right
                        moved = True
                        break
                if not moved:
                    tmpcoords[0] += movement_speed
            else:
                tmpcoords[0] -= tmpcoords[0] - (map_size * tile_size - self.size[0] / 2)

        if pressed_keys[pygame.K_z]:
            if tmpcoords[1] - movement_speed > self.size[1] / 2:
                moved = False
                for tile in rendered_tiles:
                    # check if the top of the player collides with the bottom of the tile
                    if (tile.type == "wall" or tile.type == "cactus" or tile.type == "barrel" or tile.type == "crate") and (right > tile.left) and (left < tile.right) and (top >= tile.bottom) and (top - movement_speed < tile.bottom):
                        tmpcoords[1] += tile.bottom - top
                        moved = True
                        break
                if not moved:
                    tmpcoords[1] -= movement_speed
            else:
                tmpcoords[1] -= tmpcoords[1] - self.size[1] / 2

        if pressed_keys[pygame.K_s]:
            if tmpcoords[1] + movement_speed < map_size * tile_size - self.size[1] / 2:
                moved = False
                for tile in rendered_tiles:
                    # check if the bottom of the player collides with the top of the tile
                    if (tile.type == "wall" or tile.type == "cactus" or tile.type == "barrel" or tile.type == "crate") and (right > tile.left) and (left < tile.right) and (bottom <= tile.top) and (bottom + movement_speed > tile.top):
                        tmpcoords[1] += tile.top - bottom
                        moved = True
                        break
                if not moved:
                    tmpcoords[1] += movement_speed
            else:
                tmpcoords[1] -= tmpcoords[1] - (map_size * tile_size - self.size[1] / 2)

        self.coords[0] = round(tmpcoords[0], 4)
        self.coords[1] = round(tmpcoords[1], 4)
      
        if pressed_keys[pygame.K_SPACE]:
            abilities.sendProjToServer(self.screen_width, self.screen_height, tcp_sock, self.coords, camera.coords)

        screen.blit(pygame.transform.rotate(self.surf, self.angle), (self.screen_width/2 + self.coords[0] - camera.coords[0] - self.size[0]/2, self.screen_height/2 + self.coords[1] - camera.coords[1] - self.size[1]/2))