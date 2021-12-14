import socket
import time
from socket import *

from robot_config import *


class TestOpenLoopControl:
    send_freq: int = 5  # Hz

    def __init__(self) -> None:
        super().__init__()
        self.client_socket: socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
        self.client_socket.connect((RobotIP, Port1))
        time.sleep(1)

    def ping(self) -> None:
        self.send_cmd("PING")

    def go_forward(self, power: int, seconds: int) -> None:
        self.send_cmd("MMW !M {0} -{1}".format(str(power), str(power)))
        for i in range(0, seconds * self.send_freq):
            self.ping()
        self.stop()
        time.sleep(0.2)

    def go_backward(self, power: int, seconds: int) -> None:
        self.send_cmd("MMW !M -{0} {1}".format(str(power), str(power)))
        for i in range(0, (seconds * self.send_freq) - 1):
            self.ping()
        self.stop()

    def turn_left(self, power: int, seconds: int) -> None:
        self.send_cmd("MMW !M -{0} -{1}".format(str(power), str(power)))
        for i in range(0, (seconds * self.send_freq) - 1):
            self.ping()
        self.stop()

    def turn_right(self, power: int, seconds: int) -> None:
        self.send_cmd("MMW !M {0} {1}".format(str(power), str(power)))
        for i in range(0, (seconds * self.send_freq) - 1):
            self.ping()
        self.stop()

    def wait(self, seconds: int) -> None:
        for i in range(0, seconds * self.send_freq):
            self.ping()

    def stop(self) -> None:
        self.send_cmd("MMW !M 0 0")

    def emergency_stop(self) -> None:
        self.send_cmd("MMW !M 0 0")
        self.send_cmd("MMW !EX")

    def emergency_stop_release(self) -> None:
        self.send_cmd("MMW !MG")

    def set_front_light(self, on: bool) -> None:
        if (on):
            self.send_cmd("SYS MMC 255")
        else:
            self.send_cmd("SYS MMC 127")

    def send_cmd(self, cmd: str) -> None:
        data = bytes(cmd, 'utf-8') + b'\r\n'
        # data_send: int = self.client_socket.send(data)
        # if data_send != len(data):
        #     raise RuntimeError
        self.client_socket.sendall(data)
        print(cmd)
        time.sleep(1.0/self.send_freq)

    def close_connection(self):
        self.client_socket.close()


def test_cmd():
    test = TestOpenLoopControl()
    try:
        test.emergency_stop_release()
        test.set_front_light(True)
        test.turn_left(200, 2)
        test.go_forward(200, 2)
        test.turn_right(200, 2)
        test.go_backward(200, 2)
        test.turn_left(200, 2)
        test.go_forward(200, 2)
        test.turn_right(200, 2)
        test.go_backward(200, 2)
        test.set_front_light(False)
    finally:
        test.emergency_stop()
        test.close_connection()


if __name__ == '__main__':
    test_cmd()
