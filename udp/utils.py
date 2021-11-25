# Envia um arquivo para outro socket udp
from socket import *
from typing import Tuple, TypeAlias

# constantes
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


def send_file(udp_socket: socket, file_name: str, addr: Address, buffer_size: int = 2048) -> None:
    print(f'\nPreparing to send {file_name}')
    with open(file_name, 'rb') as f:
        data = f.read(buffer_size)
        while(data):
            print(f'Uploading {file_name}...')
            if(udp_socket.sendto(data, addr)):
                data = f.read(buffer_size)
    print(f'--------------- Finished! ---------------\n')


def recv_file(udp_socket: socket, file_name: str, buffer_size: int = 2048) -> None:
    print(f'\nPreparing to recieve {file_name} \n')
    with open(file_name, 'wb') as f:
        data, _ = udp_socket.recvfrom(buffer_size)
        try:
            while(data):
                print(f'Downloading {file_name}...')
                f.write(data)
                udp_socket.settimeout(2)
                data, _ = udp_socket.recvfrom(buffer_size)
        except timeout:
            print(f'{file_name} Downloaded')
            udp_socket.settimeout(None)
    print(f'---------------- Finished! ----------------\n')
