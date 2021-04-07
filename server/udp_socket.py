import socket
import json

import coords_handler

def run(host, port, users):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((host, port))

    connected_clients = []

    while True:
        try:
            data, addr = udp_socket.recvfrom(1024)
            data = json.loads(data.decode())

            if data["type"] == "player_coords" and data["id"] == [user for user in users.values() if user["auth_token"] == data["auth_token"]][0]["id"]:
                if addr not in connected_clients:
                    connected_clients.append(addr)
                else:
                    coords_handler.coords_handler(udp_socket, data, connected_clients, addr, users)
            else:
                if addr in connected_clients:
                    connected_clients.remove(addr)
        except Exception as exception:
            print(exception)
            if addr in connected_clients:
                connected_clients.remove(addr)