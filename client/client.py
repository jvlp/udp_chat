from udp.utils import *

PREFIX = 'recieved_from_server_'
test_folder = '../test_files/'
test_files = ['teste1.txt', 'teste2.txt', 'teste3.jpg', 'teste4.txt']

def main():
    udp_socket = create_udp_socket(client_addr)
    for file_name in test_files:

        udp_socket.sendto(file_name.encode(), server_addr)
        send_file(udp_socket, test_folder + file_name, server_addr)

        file_name_fs, _ = udp_socket.recvfrom(BUFFER)
        recv_file(udp_socket, PREFIX+file_name_fs.decode())

    udp_socket.close()
    

if __name__ == '__main__':
    main()
