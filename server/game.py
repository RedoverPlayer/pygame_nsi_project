import json
import traceback
import time

class Game:
    def __init__(self, clients, users):
        self.clients = clients
        self.users = users

        stats_dict = {}
        for client in self.clients:
            stats_dict[client] = {"hp": 400, "kills": 0, "damage_dealt": 0, "damage_taken": 0, "position": [0, 0], "main_ability_timestamp": time.time()}
        self.stats_dict = stats_dict

        for client in self.clients:
            connected_users = []
            for user in [elem for elem in users if elem in self.clients and elem != client]:
                connected_users.append({"type": "player_connection", "id": users[user]["id"], "username": users[user]["username"]})
            client.send(('{"type": "multiple_players_connection", "players": ' + json.dumps(connected_users) + '}$').encode("ascii"))

        self.projs = []

    def HPChangeProjectile(self, client, hp, sender_id):
        if self.stats_dict[client]["hp"] - hp <= 0:
            self.stats_dict[[elem for elem in self.stats_dict if elem in [elem for elem in self.users if self.users[elem]["id"] == sender_id]][0]]["damage_dealt"] += hp
            self.stats_dict[[elem for elem in self.stats_dict if elem in [elem for elem in self.users if self.users[elem]["id"] == sender_id]][0]]["kills"] += 1
            self.stats_dict[client]["damage_taken"] += hp
            self.closeClient(client)
        else:
            self.stats_dict[[elem for elem in self.stats_dict if elem in [elem for elem in self.users if self.users[elem]["id"] == sender_id]][0]]["damage_dealt"] += hp
            self.stats_dict[client]["damage_taken"] += hp
            self.stats_dict[client]["hp"] -= hp
            for c in [elem for elem in self.clients if elem != client]:
                try:
                    c.send(('{"type": "remote_hp_change", "id": "' + self.users[client]["id"] + '", "hp": ' + str(self.stats_dict[client]["hp"]) + '}$').encode("ascii"))
                except:
                    print(traceback.format_exc())
            try:
                client.send(('{"type": "hp_change", "hp": ' + str(self.stats_dict[client]["hp"]) + '}$').encode("ascii"))
            except:
                print(traceback.format_exc())

    def check_clients(self, games):
        if len(self.clients) == 1:
            self.close(games)

    def close(self, games):
        classment_position = len(self.clients)
        for client in self.clients:
            try:
                client.send(('{"type": "game_ended", "classment_position": ' + str(classment_position) + ', "damage_dealt": ' + str(self.stats_dict[client]["damage_dealt"]) + ', "damage_taken": ' + str(self.stats_dict[client]["damage_taken"]) + ', "kills": ' + str(self.stats_dict[client]["kills"]) + ', "trophies": ' + str(5 - classment_position) + '}$').encode("ascii"))
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

    def closeClient(self, client):
        classment_position = len(self.clients)
        
        try:
            client.send(('{"type": "game_ended", "classment_position": ' + str(classment_position) + ', "damage_dealt": ' + str(self.stats_dict[client]["damage_dealt"]) + ', "damage_taken": ' + str(self.stats_dict[client]["damage_taken"]) + ', "kills": ' + str(self.stats_dict[client]["kills"]) + ', "trophies": ' + str(5 - classment_position) + '}$').encode("ascii"))
        except:
            print(traceback.format_exc())

        for other_client in [elem for elem in self.clients if elem != client]:
            try:
                other_client.send(('{"type": "player_disconnection", "id": "' + self.users[client]["id"] + '"}$').encode("ascii"))
            except:
                print(traceback.format_exc())
        try:
            self.clients.remove(client)
        except:
            print(traceback.format_exc())
        
        self.check_clients(self.games)

class ShowdownGame(Game):
    def __init__(self, clients, users):
        Game.__init__(self, clients, users)
        self.gamemode = "showdown"

    def update(self, users, games, tick_time, udp_sock, udp_clients):
        self.check_clients(games)
        self.games = games

        for client in self.stats_dict:
            if self.stats_dict[client]["hp"] == 0:
                self.closeClient(client, users)

        for proj in self.projs: 
            proj.update(tick_time, udp_sock, self, udp_clients, users, self.stats_dict)