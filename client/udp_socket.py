import socket
import json
import traceback

def connect(hote, port, auth_token):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Connected on the port {}".format(port))
    udp_sock.sendto(('{"type": "address_delivery", "auth_token": "' + auth_token + '"}').encode("ascii"), (hote, port))

    return udp_sock

def sendCoords(udp_sock, addr, player_coords, id, auth_token):
    udp_sock.sendto(('{"type": "player_coords", "id": "' + id + '", "auth_token": "' + auth_token + '", "coords": ' + str(player_coords) + '}').encode("ascii"), addr)

def run(udp_sock, rplayers, projs):
    while True:
        try:
            data, addr = udp_sock.recvfrom(1024)
            data = json.loads(data.decode("ascii"))

            if data[0] == "remote_coords":
                for rplayer in rplayers:
                    if rplayer.id == data[1]:
                        rplayer.coords = data[2]
            elif data[0] == "proj":
                for proj in projs:
                    if proj.id == data[1]:
                        proj.coords = data[2]
        except:
            print(traceback.format_exc())