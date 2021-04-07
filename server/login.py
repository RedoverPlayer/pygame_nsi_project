import random

def loginRequest(client, connected_clients, users):
    token = genToken(32)
    id = str(client.getpeername())
    username = client.getpeername()[0]

    
    client.send(('{"type": "account_infos", "auth_token": "' + token + '", "id": "' + id + '", "username": "' + username + '"}').encode())
    for user in users.values():
        client.send(('{"type": "player_connection", "id": "' + user["id"] + '", "username": "' + user["username"] + '"}').encode())
    users[client] = {"auth_token": token, "id": id, "username": username}
    
    for other_client in [elem for elem in connected_clients if elem != client]:
        other_client.send(('{"type": "player_connection", "id": "' + id + '", "username": "' + username + '"}').encode())

def genToken(length):
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return "".join([random.choice(characters) for _ in range(length)])