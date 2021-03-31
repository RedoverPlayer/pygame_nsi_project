import socket

def connect(hote, port):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Connected on the port {}".format(port))
    udp_sock.sendto("address_delivery".encode(), (hote, port))

    return udp_sock

def sendCoords(udp_sock, addr, player_coords):
    udp_sock.sendto(('{"type": "player_coords", "player_id": "1", "coords": ' + str(player_coords) + '}').encode(), addr)

# def receive(socket):
#     while True:
#         try:
#             data, addr = socket.recvfrom(1024)
#             data = data.decode()

#         except:
#             pass