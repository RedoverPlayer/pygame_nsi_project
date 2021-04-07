import socket
import select
import json

import event_handler
import login

def run(hote, port, users):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connection...")
    server.bind((hote, port))
    server.listen(5)
    print(f"The server is now connected on the port {port}")

    server_enabled = True
    connected_clients = []

    while server_enabled:

        waiting_connections, wlist, xlist = select.select([server], [], [], 0.05)

        for connection in waiting_connections:
            connection_with_client, connection_infos = connection.accept()
            connected_clients.append(connection_with_client)

        to_read_clients = []

        try:
            to_read_clients, wlist, xlist = select.select(connected_clients, [], [], 0.05)
        except select.error:
            pass
        else:
            for client in to_read_clients:
                try:
                    data = client.recv(1024).decode()
                    try:
                        data = json.loads(data)
                        print(data)
                        if type(data["type"]) != str:
                            print("data type not string")
                            connected_clients.remove(client)
                            client.close()

                        if data["type"] != "login" and not client in users:
                            print("Invalid request")
                            connected_clients.remove(client)
                            client.close()

                    except Exception as exception:
                        print(exception)
                        connected_clients.remove(client)
                        client.close()

                        for client in [elem for elem in connected_clients if elem != client]:
                            client.send(('{"type": "player_disconnection", "id": "' + users[client]["id"] + '"}').encode())

                        continue

                    if ["type"] == "event":
                        event_handler.event_received(data, client, users)
                    elif data["type"] == "login":
                        login.loginRequest(client, connected_clients, users)

                except Exception as exception:
                    print(exception)
                    connected_clients.remove(client)
                    client.close()

                    for client in [elem for elem in connected_clients if elem != client]:
                        client.send(('{"type": "player_disconnection", "id": "' + users[client]["id"] + '"}').encode())

                    continue

    print("Closing connections")
    for client in connected_clients:
        client.close()

    print("Connections closed")
    server.close()