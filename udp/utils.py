import struct
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


def checksum(data: bytes) -> bytes:
    checksum = 0
    data_len = len(data)
    if (data_len % 2):
        data_len += 1
        data += struct.pack('!B', 0)

    for i in range(0, data_len, 2):
        w = (data[i] << 8) + (data[i + 1])
        checksum += w

    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum = ~checksum & 0xFFFF
    # print(str(checksum).zfill(16).encode())
    return str(checksum).zfill(16).encode()


def wait_for_ack(udp_socket: socket, seg: int, buffer_size: int = 2048) -> bool:
    udp_socket.settimeout(2)
    try:
        ack_msg, _ = udp_socket.recvfrom(buffer_size)
    except timeout:
        print("Timeout")
        udp_socket.settimeout(None)
        return False
    else:
        udp_socket.settimeout(None)
        # print(ack_msg)
        ack_seg = int(ack_msg.decode())
        # print(ack_seg)
        return ack_seg == seg


def check_ack(data: bytes, seg: int) -> bool:
    expected_checksum = data[:16]
    expected_seg = chr(data[16])
    data = data[17:]
    print(f'{expected_seg=}')
    print(f'{seg%2=}')
    print(f'{expected_checksum=}')
    print(f'checksum={checksum(data)}')
    return str(seg % 2) == expected_seg and expected_checksum == checksum(data)


def create_udp_socket(addr: Address) -> socket:
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    udp_socket.bind(addr)
    return udp_socket


def send_file(udp_socket: socket, file_path: str, addr: Address, prefix: str = '', buffer_size: int = 2048) -> None:
    file_name = file_path.split('/')[-1]
    print(f'\nPreparing to send {file_name}')
    data = load_file(prefix+file_path, buffer_size)
    num_of_pkt = str(len(data))
    metadata = file_name + ':' + num_of_pkt

    udp_socket.sendto(metadata.encode(), addr)
    for seg, pkt in enumerate(data):
        pkt_counter = f'[{str(seg + 1).zfill(len(num_of_pkt))}/{num_of_pkt}]'
        print(f'{pkt_counter} Uploading {file_name}...')
        ack_received = False
        while not ack_received:
            udp_socket.sendto(checksum(pkt) + str(seg % 2).encode() + pkt, addr)
            ack_received = wait_for_ack(udp_socket, seg, buffer_size)
    udp_socket.settimeout(None)
    print(f'--------------- Finished! ---------------\n')


def recv_file(udp_socket: socket, prefix: str = '',  buffer_size: int = 2048) -> Tuple[str, Address]:
    metadata, addr = udp_socket.recvfrom(buffer_size)
    file_name, num_of_pkt = metadata.decode().split(':')
    num_of_pkt = int(num_of_pkt)
    print(f'\nPreparing to receive {file_name} \n')

    file = list()

    for seg in range(0, num_of_pkt):
        pkt_counter = f'[{str(seg + 1).zfill(len(str(num_of_pkt)))}/{num_of_pkt}]'
        print(f'{pkt_counter} Downloading {file_name}...')
        data, _ = udp_socket.recvfrom(buffer_size)
        if check_ack(data, seg):
            data = data[17:]
            udp_socket.sendto(str(seg).encode(), addr)
            file.append(data)

    print(f'{file_name} Downloaded')
    write_file(file, prefix+file_name)
    print(f'---------------- Finished! ----------------\n')

    return file_name, addr
