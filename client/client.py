from pathlib import Path

from rdt.udp import *

PREFIX = 'received_from_server_'
test_folder = Path('../test_files/')

def main():
    udp_socket = create_udp_socket(client_addr)
    for file in test_folder.iterdir():
        send_file(udp_socket, str(file.as_posix()), server_addr)
        recv_file(udp_socket, PREFIX)

    udp_socket.close()


if __name__ == '__main__':
    main()
