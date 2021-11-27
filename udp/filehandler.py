from typing import List


def load_file(file_path: str, pkt_size: int = 2048) -> List:
    file = list()
    with open(file_path, 'rb') as f:
        data = f.read(pkt_size)
        file.append(data)
        while(data):
            data = f.read(pkt_size)
            file.append(data)
    print(f'{file_path} read from disk!')
    return file[:-1]


def write_file(file: List, file_path: str) -> None:
    with open(file_path, 'wb') as f:
        for pckt in file:
            f.write(pckt)
    print(f'{file_path} saved to disk!')
