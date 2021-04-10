import socket

def connect(hote, port, auth_token):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Connected on the port {}".format(port))
    udp_sock.sendto(('{"type": "address_delivery", "auth_token": "' + auth_token + '"}').encode(), (hote, port))

    return udp_sock

def sendCoords(udp_sock, addr, player_coords, id, auth_token):
    udp_sock.sendto(('{"type": "player_coords", "id": "' + id + '", "auth_token": "' + auth_token + '", "coords": ' + str(player_coords) + '}').encode(), addr)