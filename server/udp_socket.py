import socket
import json
import traceback

import coords_handler

def run(host, port, users):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((host, port))

    connected_clients = []

    while True:
        try:
            data, addr = udp_socket.recvfrom(1024)
            data = json.loads(data.decode())

            for elem in connected_clients:
                if elem["auth_token"] not in [elem["auth_token"] for elem in users.values()]:
                    removeIfInConnectedClients(elem["auth_token"], elem["addr"], connected_clients)

            if data["auth_token"] in [elem["auth_token"] for elem in users.values()]:
                if addIfNotInConnectedClients(data, addr, connected_clients):
                    coords_handler.coords_handler(udp_socket, data, connected_clients, addr, users)
            elif data["type"] == "address_delivery":
                addIfNotInConnectedClients(data, addr, connected_clients)
            else:
                removeIfInConnectedClients(data, addr, connected_clients)
        except Exception as exception:
            print(traceback.format_exc())

def addIfNotInConnectedClients(data, addr, connected_clients):
    if {"addr": addr, "auth_token": data["auth_token"]} not in connected_clients:
        connected_clients.append({"addr": addr, "auth_token": data["auth_token"]})
        return False
    else:
        return True

def removeIfInConnectedClients(auth_token, addr, connected_clients):
    if {"addr": addr, "auth_token": auth_token} in connected_clients:
        connected_clients.remove({"addr": addr, "auth_token": auth_token})