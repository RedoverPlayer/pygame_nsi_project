import random
import math
import traceback

class Projectile:
    def __init__(self, coords, angle, game, sender_id, type="regular"):
        self.coords = coords
        self.angle = angle
        if type == "regular":
            self.damage = 40
        else:
            self.damage = 150
        self.sender_id = sender_id
        self.type = type

        while True:
            self.id = genToken(8)
            if self.id not in [proj.id for proj in game.projs]:
                break

        for client in game.clients:
            try:
                client.send(('{"type": "add_proj", "id": "' + self.id + '", "proj_type": "' + self.type + '", "coords": ' + str(self.coords) + ', "angle": ' + str(self.angle) + '}$').encode("ascii"))
            except:
                print(traceback.format_exc())

    def wallOrPlayerCollision(self, game):
        game.projs.remove(self)
        for client in game.clients:
            try:
                client.send(('{"type": "remove_proj", "id": "' + self.id + '"}$').encode("ascii"))
            except:
                print(traceback.format_exc())

    def update(self, tick_time, udp_sock, game, udp_clients, users, stats_dict):
        if self.type == "regular":
            self.coords[0] += math.cos(self.angle) * tick_time
            self.coords[1] += math.sin(self.angle) * tick_time
        else:
            self.coords[0] += math.cos(self.angle) * tick_time * 4
            self.coords[1] += math.sin(self.angle) * tick_time * 4        

        if self.coords[0] < 0 or self.coords[0] > 4800 or self.coords[1] < 0 or self.coords[1] > 4800:
            self.wallOrPlayerCollision(game)
        else:
            for c, data in stats_dict.items():
                if users[c]["id"] != self.sender_id and (self.coords[0] > data["position"][0] - 30 and self.coords[0] < data["position"][0] + 30) and (self.coords[1] > data["position"][1] - 30 and self.coords[1] < data["position"][1] + 30):
                    game.HPChangeProjectile(c, self.damage, self.sender_id)
                    self.wallOrPlayerCollision(game)
                    break
            for tile in game.map.getTilesAroundCoords(self.coords):
                if (tile.type in ("wall", "cactus", "barrel", "crate")) and (self.coords[1] > tile.top) and (self.coords[1] < tile.bottom) and (self.coords[0] > tile.left) and (self.coords[0] < tile.right):
                    self.wallOrPlayerCollision(game)
            for client in game.clients:
                if users[client]["auth_token"] in [elem["auth_token"] for elem in udp_clients]:
                    udp_sock.sendto((f'["proj", "{self.id}", {self.coords}]').encode("ascii"), [elem["addr"] for elem in udp_clients if elem["auth_token"] == users[client]["auth_token"]][0])

def genToken(length):
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return "".join([random.choice(characters) for _ in range(length)])