import json

def coords_handler(udp_socket, data, connected_clients, addr):
    data = json.loads(data) 
    if data["type"] == "player_coords":
        for client in [address for address in connected_clients if address != addr]:
            udp_socket.sendto(('{"type": "remote_coords", "player_id": ' + data["player_id"] + ', "coords": ' + str(data["coords"]) + '}').encode(), client)