import json
import traceback

def coords_handler(udp_socket, data, connected_clients, addr, new=False):
    if data["type"] == "player_coords":
        for client in [elem["addr"] for elem in connected_clients if elem["addr"] != addr]:
            try:
                udp_socket.sendto(('{"type": "remote_coords", "id": "' + data["id"] + '", "coords": ' + str(data["coords"]) + '}').encode(), client)
            except:
                connected_clients.remove([address for address in connected_clients if address == client][0])