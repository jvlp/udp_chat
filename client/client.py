from udp.utils import *

PREFIX = 'received_from_server_'
test_folder = '../test_files/'
test_files = ['teste1.txt', 'teste2.txt', 'teste3.jpg', 'teste4.txt']


def main():
    udp_socket = create_udp_socket(client_addr)
    for file_name in test_files:

        send_file(udp_socket, test_folder + file_name, server_addr)
        recv_file(udp_socket, PREFIX)

    udp_socket.close()


if __name__ == '__main__':
    main()
