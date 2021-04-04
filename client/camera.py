import time

class Camera:
    def __init__(self, width, height, map_size, tile_size):
        self.coords = [width // 2 - tile_size, height // 2 - tile_size]
        # self.coords = [(map_size * tile_size) // 2, (map_size * tile_size) // 2]
        self.width = width
        self.height = height
    
    def update(self, coords, map_size, tile_size):
        x = coords[0] >= self.width // 2 - tile_size and coords[0] <= map_size * tile_size - self.width // 2 + tile_size
        y = coords[1] >= self.height // 2 - tile_size and coords[1] <= map_size * tile_size - self.height // 2 + tile_size

        if x and not y:
            self.coords = (coords[0], self.coords[1])
        elif y and not x:
            self.coords = (self.coords[0], coords[1])
        elif x and y:
            self.coords = (coords[0], coords[1])
        else:
            self.coords = (self.coords[0], self.coords[1])

    def coords_update(self, coords):
        self.coords = coords

def move_camera_to(target_coords, map_size, tile_size, cinematic, camera):
    cinematic = True
    start_speed = ((target_coords[0] - camera.coords[0]) / 2000, (target_coords[1] - camera.coords[1]) / 2000)
    initial_coords = camera.coords
    speed = (0, 0)
    camera_coords = camera.coords

    while True:
        speed = (speed[0] + start_speed[0] / 100, speed[1] + start_speed[1] / 100)
        if target_coords[0] < initial_coords[0]:
            if camera_coords[0] > target_coords[0] / 2 + initial_coords[0] / 2:
                camera.coords_update((int(camera.coords[0] + speed[0]), int(camera.coords[1] + speed[1])))
                camera_coords = (camera_coords[0] + speed[0], camera_coords[1] + speed[1])
            else:
                break
        else:
            if camera_coords[0] < target_coords[0] / 2 + initial_coords[0] / 2:
                camera.coords_update((int(camera.coords[0] + speed[0]), int(camera.coords[1] + speed[1])))
                camera_coords = (camera_coords[0] + speed[0], camera_coords[1] + speed[1])
            else:
                break            
        time.sleep(0.005)

    while True:
        speed = (speed[0] - start_speed[0] / 100, speed[1] - start_speed[1] / 100)
        if target_coords[0] < initial_coords[0]:
            if camera_coords[0] > target_coords[0]:
                camera.coords_update((int(camera.coords[0] + speed[0]), int(camera.coords[1] + speed[1])))
                camera_coords = (camera_coords[0] + speed[0], camera_coords[1] + speed[1])
            else:
                break
        else:
            if camera_coords[0] < target_coords[0]:
                camera.coords_update((int(camera.coords[0] + speed[0]), int(camera.coords[1] + speed[1])))
                camera_coords = (camera_coords[0] + speed[0], camera_coords[1] + speed[1])
            else:
                break            
        time.sleep(0.005)
    cinematic = False