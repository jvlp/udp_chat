from rdt.udp import *

PREFIX = 'received_from_client_'


def main():
    udp_socket = create_udp_socket(server_addr)

    while True:

        file_name, addr = recv_file(udp_socket, PREFIX)
        send_file(udp_socket, file_name, addr, PREFIX)

    # udp_socket.close()


if __name__ == '__main__':
    main()
