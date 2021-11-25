from udp.utils import *

PREFIX = 'recieved_from_client_'


def main():
    udp_socket = create_udp_socket(server_addr)

    while True:
        file_name, addr = udp_socket.recvfrom(BUFFER)
        recv_file(udp_socket, PREFIX+file_name.decode())

        udp_socket.sendto(file_name, addr)
        send_file(udp_socket, PREFIX+file_name.decode(), addr)

    # udp_socket.close()


if __name__ == '__main__':
    main()
