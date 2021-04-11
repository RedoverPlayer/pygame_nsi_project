import random
import json

def loginRequest(client, connected_clients, users):
    token = genToken(32)
    id = str(client.getpeername())
    username = client.getpeername()[0]

    # sending login infos to client
    client.send(('{"type": "account_infos", "auth_token": "' + token + '", "id": "' + id + '", "username": "' + username + '"}').encode())    

    # sending to client others already connected clients
    connected_users = []
    for user in users.values():
        connected_users.append({"type": "player_connection", "id": user["id"], "username": user["username"]})
    client.send(('{"type": "multiple_players_connection", "players": ' + json.dumps(connected_users) + '}').encode())
    
    # adding client to users
    users[client] = {"auth_token": token, "id": id, "username": username}
    
    # sending connection to already connected clients
    for other_client in [elem for elem in connected_clients if elem != client]:
        other_client.send(('{"type": "player_connection", "id": "' + id + '", "username": "' + username + '"}').encode())

def genToken(length):
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return "".join([random.choice(characters) for _ in range(length)])