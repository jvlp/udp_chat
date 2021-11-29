import struct
from socket import socket, timeout
from typing import List


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


def wait_for_ack(udp_socket: socket, seq: int, buffer_size: int = 2048) -> bool:
    '''Try to receive a ACK from a udp socket, if no response is received return False.

    Args:
        udp_socket (socket): Socket that is waiting for ACK.
        seq (int): Current sequence number.
        buffer_size (int, optional): Defaults to 2048.

    Returns:
        bool: Whether ACK was received correctly or not.
    '''
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
        ack_seq = int(ack_msg.decode())
        # print(ack_seq)
        return ack_seq == seq


def check_ack(data: bytes, seq: int) -> bool:
    expected_checksum = data[:16]
    expected_seq = chr(data[16])
    data = data[17:]
    # print(f'{expected_seq=}')
    # print(f'{seq%2=}')
    # print(f'{expected_checksum=}')
    # print(f'checksum={checksum(data)}')
    return str(seq % 2) == expected_seq and expected_checksum == checksum(data)


def load_file(file_path: str, pkt_size: int = 2048) -> List[bytes]:
    file = list()
    pkt_num = 0
    with open(file_path, 'rb') as f:
        data = f.read(pkt_size - 17)
        file.append(data)
        while(data):
            pkt_num += 1
            data = f.read(pkt_size - 17)
            file.append(data)
    print(f'{file_path} read from disk!')
    return file[:-1]


def write_file(file: List[bytes], file_path: str) -> None:
    with open(file_path, 'wb') as f:
        for pckt in file:
            f.write(pckt)
    print(f'{file_path} saved to disk!')
