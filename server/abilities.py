import random
import math
import traceback

class Projectile:
    def __init__(self, coords, angle, game):
        self.coords = coords
        self.angle = angle

        while True:
            self.id = genToken(8)
            if self.id not in [proj.id for proj in game.projs]:
                break

        for client in game.clients:
            try:
                client.send(('{"type": "add_proj", "id": "' + self.id + '", "coords": ' + str(self.coords) + ', "angle": ' + str(self.angle) + '}$').encode("ascii"))
            except:
                print(traceback.format_exc())

    def update(self, tick_time, udp_sock, game, udp_clients, users):
        self.coords[0] += math.cos(self.angle) * tick_time
        self.coords[1] += math.sin(self.angle) * tick_time

        if self.coords[0] < 0 or self.coords[0] > 4800 or self.coords[1] < 0 or self.coords[1] > 4800:
            game.projs.remove(self)
            for client in game.clients:
                try:
                    client.send(('{"type": "remove_proj", "id": "' + self.id + '"}$').encode("ascii"))
                except:
                    print(traceback.format_exc())
        else:
            for client in game.clients:
                if users[client]["auth_token"] in [elem["auth_token"] for elem in udp_clients]:
                    udp_sock.sendto((f'["proj", "{self.id}", {self.coords}]').encode("ascii"), [elem["addr"] for elem in udp_clients if elem["auth_token"] == users[client]["auth_token"]][0])

def genToken(length):
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return "".join([random.choice(characters) for _ in range(length)])