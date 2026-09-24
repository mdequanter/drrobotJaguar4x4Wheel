import socket
import time
from socket import *

from robot_config import *

# !M takes -1000..1000, so this is a percentage of full throttle * 10.
# Measured on the floor: 200 gives only ~0.26 m/s, which looks like the robot
# barely moves. 600 is a usable open-loop speed.
DRIVE_POWER: int = 200
MAX_POWER: int = 1000


class TestOpenLoopControl:
    send_freq: int = 5  # Hz

    def __init__(self) -> None:
        super().__init__()
        self.client_socket: socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
        self.client_socket.connect((RobotIP, Port1))
        time.sleep(1)

    def ping(self) -> None:
        self._send("PING")

    def go_forward(self, power: int, seconds: float) -> None:
        self._drive(power, -power, seconds)

    def go_backward(self, power: int, seconds: float) -> None:
        self._drive(-power, power, seconds)

    def turn_left(self, power: int, seconds: float) -> None:
        self._drive(-power, -power, seconds)

    def turn_right(self, power: int, seconds: float) -> None:
        self._drive(power, power, seconds)

    def wait(self, seconds: float) -> None:
        self._hold(seconds)

    def stop(self) -> None:
        self.send_cmd("MMW !M 0 0")

    def emergency_stop(self) -> None:
        """Latches !EX on both boards. Only recoverable with emergency_stop_release()."""
        self.send_cmd("MMW !M 0 0")
        self.send_cmd("MMW !EX")

    def emergency_stop_release(self) -> None:
        self.send_cmd("MMW !MG")

    def set_front_light(self, on: bool) -> None:
        if (on):
            self.send_cmd("SYS MMC 255")
        else:
            self.send_cmd("SYS MMC 127")

    def _drive(self, left: int, right: int, seconds: float) -> None:
        left = max(-MAX_POWER, min(MAX_POWER, int(left)))
        right = max(-MAX_POWER, min(MAX_POWER, int(right)))
        self._send("MMW !M {0} {1}".format(left, right))
        self._hold(seconds)
        self.stop()

    def _hold(self, seconds: float) -> None:
        """Block for exactly `seconds` of wall-clock time, pinging at send_freq.

        The motor boards run with their serial watchdog disabled (~RWD reports
        RWD=0), so the pings do not sustain motion -- the last !M holds on its
        own. They only keep the link active while we wait out the duration.
        """
        period = 1.0 / self.send_freq
        deadline = time.time() + seconds
        tick = time.time()
        while True:
            tick += period
            if tick >= deadline:
                time.sleep(max(0.0, deadline - time.time()))
                return
            time.sleep(max(0.0, tick - time.time()))
            self.ping()

    def _send(self, cmd: str) -> None:
        """Write one command line. Does not pace -- callers time themselves."""
        self.client_socket.sendall(bytes(cmd, 'utf-8') + b'\r\n')
        print(cmd)

    def send_cmd(self, cmd: str) -> None:
        """Send one command and leave a 1/send_freq gap before the next one."""
        self._send(cmd)
        time.sleep(1.0 / self.send_freq)

    def close_connection(self):
        self.client_socket.close()


def test_cmd():
    test = TestOpenLoopControl()
    try:
        test.emergency_stop_release()
        test.set_front_light(True)
        #test.turn_left(DRIVE_POWER, 2)
        test.go_forward(DRIVE_POWER, 2)
        test.turn_right(DRIVE_POWER*1.5, 3)
        test.go_forward(DRIVE_POWER, 2)
        test.turn_right(DRIVE_POWER*1.5, 3)
        #test.turn_left(DRIVE_POWER, 2)
        #test.go_forward(DRIVE_POWER, 2)
        #test.turn_right(DRIVE_POWER, 2)
        #test.go_backward(DRIVE_POWER, 2)
        test.set_front_light(False)
    finally:
        # stop(), not emergency_stop(): !EX latches and would leave the robot
        # dead to the next client until someone sends !MG.
        test.stop()
        test.close_connection()


if __name__ == '__main__':
    test_cmd()
