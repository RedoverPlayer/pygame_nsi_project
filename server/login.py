import random
import json

def loginRequest(client, connected_clients, users):
    token = genToken(32)
    id = str(client.getpeername())
    username = client.getpeername()[0]

    # sending login infos to client
    client.send(('{"type": "account_infos", "auth_token": "' + token + '", "id": "' + id + '", "username": "' + username + '"}').encode("ascii"))    
    
    # adding client to users
    users[client] = {"auth_token": token, "id": id, "username": username}

def genToken(length):
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return "".join([random.choice(characters) for _ in range(length)])