import socket
import select
import json
import traceback

import event_handler
import login

def removeClient(client, tcp_clients, users):
    tcp_clients.remove(client)

    if client in users:
        for other_client in [elem for elem in tcp_clients if elem != client]:
            other_client.send(('{"type": "player_disconnection", "id": "' + users[client]["id"] + '"}').encode())
        del users[client]

    client.close()

def run(hote, port, users):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connection...")
    server.bind((hote, port))
    server.listen(5)
    print(f"The server is now connected on the port {port}")

    server_enabled = True
    tcp_clients = []

    while server_enabled:
        waiting_connections, wlist, xlist = select.select([server], [], [], 0.05)

        for connection in waiting_connections:
            connection_with_client, connection_infos = connection.accept()
            tcp_clients.append(connection_with_client)

        to_read_clients = []

        try:
            to_read_clients, wlist, xlist = select.select(tcp_clients, [], [], 0.05)
        except:
            pass
        else:
            for client in to_read_clients:
                try:
                    data = client.recv(1024).decode()
                    print(data)
                    try:
                        if data != "":
                            data = json.loads(data)
                            if type(data["type"]) != str:
                                print("data type not string")
                                removeClient(client, tcp_clients, users)

                            if data["type"] != "login" and not client in users:
                                print("Invalid request")
                                removeClient(client, tcp_clients, users)

                            if data["type"] == "event":
                                event_handler.event_received(data, client, users)
                            elif data["type"] == "login":
                                login.loginRequest(client, tcp_clients, users)

                    except Exception as exception:
                        print(traceback.format_exc())
                        removeClient(client, tcp_clients, users)

                        continue

                except socket.error:
                    print(traceback.format_exc())
                    removeClient(client, tcp_clients, users)
                except Exception as exception:
                    print(traceback.format_exc())

    print("Closing connections")
    for client in tcp_clients:
        client.close()

    print("Connections closed")
    server.close()