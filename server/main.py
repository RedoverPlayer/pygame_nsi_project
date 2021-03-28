import socket
import select

import coords_handler

host = ""
port = 12861

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((host, port))

connected_clients = []

while True:
    try:
        data, addr = udp_socket.recvfrom(1024)
        data = data.decode()
        print(addr, data)
        if addr not in connected_clients:
            connected_clients.append(addr)
        coords_handler.coords_handler(udp_socket, data, connected_clients, addr)
    except Exception as exception:
        print(exception)

# TCP socket, finishing it later

# hote = ''
# port = 12860

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print("Connection...")
# server.bind((hote, port))
# server.listen(5)
# print(f"The server is now connected on the port {port}")

# server_enabled = True
# connected_clients = []

# while server_enabled:

#     waiting_connections, wlist, xlist = select.select([server], [], [], 0.05)

#     for connection in waiting_connections:
#         connection_with_client, connection_infos = connection.accept()
#         connected_clients.append(connection_with_client)

#     to_read_clients = []

#     try:
#         to_read_clients, wlist, xlist = select.select(connected_clients, [], [], 0.05)
#     except select.error:
#         pass
#     else:
#         for client in to_read_clients:
#             try:
#                 data = client.recv(1024).decode()
#                 print(data)
#                 coords_handler.coords_handler(client, data, connected_clients)
#             except Exception as exception:
#                 print(exception)
#                 # continue

# print("Closing connections")
# for client in connected_clients:
#     client.close()

# print("Connections closed")
# server.close()