import json

class Game:
    def __init__(self, clients, users):
        self.clients = clients

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
        for client in self.clients:
            client.send('{"type": "game_ended"}$'.encode())
        games.remove(self)

    def removeClient(self, client, users):
        for other_client in [elem for elem in self.clients if elem != client]:
            other_client.send(('{"type": "player_disconnection", "id": "' + users[client]["id"] + '"}$').encode())
        self.clients.remove(client)

class ShowdownGame(Game):
    def __init__(self, clients, users):
        Game.__init__(self, clients, users)
        self.gamemode = "showdown"

    def update(self, users, games):
        self.check_clients(users, games)