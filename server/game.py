import json
import traceback

class Game:
    def __init__(self, clients, users):
        self.clients = clients

        stats_dict = {}
        for client in self.clients:
            stats_dict[client] = {"hp": 400, "kills": 0, "position": [0, 0]}
        self.stats_dict = stats_dict

        for client in self.clients:
            connected_users = []
            for user in [elem for elem in users if elem in self.clients and elem != client]:
                connected_users.append({"type": "player_connection", "id": users[user]["id"], "username": users[user]["username"]})
            client.send(('{"type": "multiple_players_connection", "players": ' + json.dumps(connected_users) + '}$').encode())

    def playerDisconnect(self):
        pass

    def PVChange(self, client):
        client.send()

    def check_clients(self, users, games):
        if len(self.clients) == 1:
            self.close(games)

    def close(self, games):
        classment_position = len(self.clients)
        for client in self.clients:
            try:
                client.send(('{"type": "game_ended", "classment_position": ' + str(classment_position) + ', "kills": ' + str(self.stats_dict[client]["kills"]) + ', "trophies": 0}$').encode())
            except:
                print(traceback.format_exc())
        games.remove(self)

    def removeClient(self, client, users):
        for other_client in [elem for elem in self.clients if elem != client]:
            try:
                other_client.send(('{"type": "player_disconnection", "id": "' + users[client]["id"] + '"}$').encode())
            except:
                print(traceback.format_exc())
        self.clients.remove(client)
        del self.stats_dict[client]

    def closeClient(self, client, users):
        classment_position = len(self.clients)
        try:
            client.send(('{"type": "game_ended", "classment_position": ' + str(classment_position) + ', "kills": ' + str(self.stats_dict[client]["kills"]) + ', "trophies": 0}$').encode())
        except:
            print(traceback.format_exc())

        for other_client in [elem for elem in self.clients if elem != client]:
            try:
                other_client.send(('{"type": "player_disconnection", "id": "' + users[client]["id"] + '"}$').encode())
            except:
                print(traceback.format_exc())
        self.clients.remove(client)

class ShowdownGame(Game):
    def __init__(self, clients, users):
        Game.__init__(self, clients, users)
        self.gamemode = "showdown"

    def update(self, users, games):
        self.check_clients(users, games)
        for client in self.stats_dict:
            if self.stats_dict[client]["hp"] == 0:
                self.closeClient(client, users)
