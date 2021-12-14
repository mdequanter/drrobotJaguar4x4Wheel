import socket
from socket import *

from robot_config import *


def test_socket():
    client_socket: socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
    print("try connect")
    client_socket.connect((RobotIP, Port1))
    data: bytes = b"PING\r\n"
    data_send: int = client_socket.send(data)
    print("success = " + str(data_send == len(data)))

    client_socket.close()


if __name__ == '__main__':
    test_socket()
