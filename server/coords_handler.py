import json
import traceback

def coords_handler(udp_socket, data, connected_clients, addr, users, games):
    if data["type"] == "player_coords":
        for game in games:
            for client in game.clients:
                if users[client]["id"] == data["id"] and users[client]["auth_token"] == data["auth_token"]:
                    tmp = client
            for c in [elem for elem in connected_clients if elem["auth_token"] in [users[elem]["auth_token"] for elem in users if elem in game.clients and elem != tmp]]:
                udp_socket.sendto(('{"type": "remote_coords", "id": "' + data["id"] + '", "coords": ' + str(data["coords"]) + '}').encode(), c["addr"])