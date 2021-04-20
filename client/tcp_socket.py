import socket
import json
import time
import traceback

import remote_player

def connect(hote, port, vars, ui_status):
    while True:
        try:
            ui_status[0] = "connecting"
            connection_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Connection...")
            connection_with_server.connect((hote, port))
            print("Connected on the port {}".format(port))

            connection_with_server.send('{"type": "login"}'.encode())
            data = json.loads(connection_with_server.recv(1024).decode())
            break
        except:
            ui_status[0] = "connection_failed"
            time.sleep(5)

    vars += [data["username"], data["id"], data["auth_token"], connection_with_server]
    ui_status[0] = "main_menu"

def run(connection_with_server, id, auth_token, rplayers, screen_width, screen_height, events, event_lock):
    while True:
        try:
            data_list = connection_with_server.recv(1024).decode().split("$")
            for elem in [elem for elem in data_list if elem != ""]:
                data = json.loads(elem)
                print(data)

                if data["type"] == "player_connection":
                    rplayers.append(remote_player.RemotePlayer(screen_width, screen_height, data["id"], data["username"]))
                elif data["type"] == "multiple_players_connection":
                    for player in data["players"]:
                        rplayers.append(remote_player.RemotePlayer(screen_width, screen_height, player["id"], player["username"]))
                elif data["type"] ==  "player_disconnection":
                    rplayers.remove([rplayer for rplayer in rplayers if rplayer.id == data["id"]][0])
                else:
                    event_lock.acquire()
                    events.append(data)
                    event_lock.release()
        except:
            pass