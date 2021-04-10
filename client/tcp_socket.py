import socket
import json
import traceback
import remote_player

def connect(hote, port):
    connection_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connection...")
    connection_with_server.connect((hote, port))
    print("Connected on the port {}".format(port))

    connection_with_server.send('{"type": "login"}'.encode())
    data = json.loads(connection_with_server.recv(1024).decode())

    return data["id"], data["auth_token"], connection_with_server

def run(connection_with_server, id, auth_token, rplayers, screen_width, screen_height):
    while True:
        try:
            data = connection_with_server.recv(1024).decode()
            data = json.loads(data)

            if data["type"] == "player_connection":
                rplayers.append(remote_player.RemotePlayer(screen_width, screen_height, data["id"], data["username"]))
            elif data["type"] == "multiple_players_connection":
                for player in data["players"]:
                    rplayers.append(remote_player.RemotePlayer(screen_width, screen_height, player["id"], player["username"]))
            elif data["type"] ==  "player_disconnection":
                rplayers.remove([rplayer for rplayer in rplayers if rplayer.id == data["id"]][0])
        except:
            pass