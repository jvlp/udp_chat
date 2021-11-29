from socket import socket, AF_INET, SOCK_DGRAM
from typing import Tuple

from rdt.utils import check_ack, checksum, load_file, wait_for_ack, write_file

HOST = '127.0.0.1'
BUFFER = 2048
CLIENT_PORT = 3000
SERVER_PORT = 2000
server_addr = (HOST, SERVER_PORT)
client_addr = (HOST, CLIENT_PORT)

Address = Tuple[str, int]


def create_udp_socket(addr: Address) -> socket:
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    udp_socket.bind(addr)
    return udp_socket


def send_file(udp_socket: socket, file_path: str, addr: Address, prefix: str = '', buffer_size: int = 2048) -> None:
    file_name = file_path.split('/')[-1]
    print(f'\nPreparing to send {file_name}')
    data = load_file(prefix + file_path, buffer_size)
    num_of_pkt = str(len(data))
    metadata = file_name + ':' + num_of_pkt

    udp_socket.sendto(metadata.encode(), addr)
    for seq, pkt in enumerate(data):
        pkt_counter = f'[{str(seq + 1).zfill(len(num_of_pkt))}/{num_of_pkt}]'
        print(f'{pkt_counter} Uploading {file_name}...')
        ack_received = False
        while not ack_received:
            udp_socket.sendto(checksum(pkt) + str(seq % 2).encode() + pkt, addr)
            ack_received = wait_for_ack(udp_socket, seq, buffer_size)
    udp_socket.settimeout(None)
    print(f'--------------- Finished! ---------------\n')


def recv_file(udp_socket: socket, prefix: str = '',  buffer_size: int = 2048) -> Tuple[str, Address]:
    metadata, addr = udp_socket.recvfrom(buffer_size)
    file_name, num_of_pkt = metadata.decode().split(':')
    print(f'\nPreparing to receive {file_name} \n')

    file = list()

    for seq in range(0, int(num_of_pkt)):
        pkt_counter = f'[{str(seq + 1).zfill(len(num_of_pkt))}/{num_of_pkt}]'
        print(f'{pkt_counter} Downloading {file_name}...')
        data, _ = udp_socket.recvfrom(buffer_size)
        if check_ack(data, seq):
            data = data[17:]
            udp_socket.sendto(str(seq).encode(), addr)
            file.append(data)

    print(f'{file_name} Downloaded')
    write_file(file, prefix+file_name)
    print(f'---------------- Finished! ----------------\n')

    return file_name, addr
