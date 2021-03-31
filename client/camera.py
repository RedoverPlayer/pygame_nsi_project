class Camera:
    def __init__(self, width, height):
        self.coords = [0, 0]
        self.width = width
        self.height = height
    
    def update(self, coords):
        self.coords = coords