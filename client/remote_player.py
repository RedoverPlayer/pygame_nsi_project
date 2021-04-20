from character import Character

class RemotePlayer(Character):
    def __init__(self, screen_width, screen_height, id, username="Unnamed player", size=(60, 60)) -> None:
        Character.__init__(self, screen_width, screen_height, username, size)
        self.id = id

    def update(self, screen, coords):
        if ((self.coords[0] - coords[0]) + self.screen_width / 2) > -1 * self.size[0] and ((self.coords[0] - coords[0]) + self.screen_width / 2) < self.screen_width and (-1 * coords[1] + self.coords[1]) + self.screen_height / 2 > -1 * self.size[1] and (-1 * coords[1] + self.coords[1]) + self.screen_height / 2 < self.screen_height + self.size[1]:
            self.render(screen, coords)