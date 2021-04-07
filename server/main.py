import threading
import tcp_socket
import udp_socket

def tcp_socket_thread(users):
    while True:
        # try:
        tcp_socket.run('', 12860, users)
        # except Exception as exception:
        #     print(exception)

def udp_socket_thread(users):
    while True:
        # try:
        udp_socket.run('', 12861, users)
        # except Exception as exception:
        #     print(exception)

if __name__ == "__main__":
    users = {}

    thread_1 = threading.Thread(target=tcp_socket_thread, args=[users])
    thread_2 = threading.Thread(target=udp_socket_thread, args=[users])

    thread_1.start()
    thread_2.start()