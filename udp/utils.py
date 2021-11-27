from socket import *
from typing import Tuple, TypeAlias

from udp.filehandler import load_file, write_file

HOST = '127.0.0.1'
BUFFER = 2048
CLIENT_PORT = 3000
SERVER_PORT = 2000
server_addr = (HOST, SERVER_PORT)
client_addr = (HOST, CLIENT_PORT)

Address: TypeAlias = Tuple[str, int]


def create_udp_socket(addr: Address) -> socket:
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    udp_socket.bind(addr)
    return udp_socket


def send_file(udp_socket: socket, file_path: str, addr: Address, prefix: str = '', buffer_size: int = 2048) -> None:
    file_name = file_path.split('/')[-1]
    print(f'\nPreparing to send {file_name}')
    data = load_file(prefix+file_path, buffer_size)
    metadata = file_name + ':' + str(len(data))

    udp_socket.sendto(metadata.encode(), addr)
    for seg, pkt in enumerate(data):
        print(f'[{seg + 1}/{len(data)}] Uploading {file_name}...')
        udp_socket.sendto(pkt, addr)
    print(f'--------------- Finished! ---------------\n')


def recv_file(udp_socket: socket, prefix: str = '',  buffer_size: int = 2048) -> Tuple[str, Address]:
    metadata, addr = udp_socket.recvfrom(BUFFER)
    file_name, num_of_pkt = metadata.decode().split(':')
    num_of_pkt = int(num_of_pkt)
    print(f'\nPreparing to receive {file_name} \n')

    file = list()

    for seg in range(0, num_of_pkt):
        print(f'[{seg + 1}/{num_of_pkt}] Downloading {file_name}...')
        data, _ = udp_socket.recvfrom(buffer_size)
        file.append(data)
    print(f'{file_name} Downloaded')
    write_file(file, prefix+file_name)
    print(f'---------------- Finished! ----------------\n')

    return file_name, addr
