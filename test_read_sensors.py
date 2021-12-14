import socket
from socket import *
from typing import AnyStr

from robot_config import *


class TestReadSensors():
    def __init__(self) -> None:
        super().__init__()
        self.client_socket: socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
        self.client_socket.connect((RobotIP, Port1))
        # self.client_socket.setblocking(False)

    def test_read(self):
        sockFile = self.client_socket.makefile()

        for i in range(0, 1000):
            message = sockFile.readline().rstrip()
            self.process(message)

    def process(self, message: AnyStr):
        if (message.startswith('#')):
            self.process_IMU_message(message)
        elif (message.startswith('MM')):
            self.process_motor_message(message)
        elif (message.startswith('$')):
            self.process_GPS_message(message)

    def process_IMU_message(self, message: AnyStr) -> None:
        print(message)

    def process_motor_message(self, message: AnyStr) -> None:
        """
        :param message: MMX Y=Z   (X = motor driver board id (0=front) or (1=rear) , Y = parameter name, Z = parameter
        (MMX ?Y messages will be ignored)
        """
        driver_board_id = int(message[2])

        if (message[4:].startswith('A=')):
            self.process_motor_current(driver_board_id, message[6:])
        elif (message[4:].startswith('AI=')):
            # digital input
            pass
        elif (message[4:].startswith('C=')):
            self.process_motor_encoder_position_count(driver_board_id, message[6:])
        elif (message[4:].startswith('D=')):
            # digital input
            pass
        elif (message[4:].startswith('P=')):
            self.process_motor_output_power(driver_board_id, message[6:])
        elif (message[4:].startswith('S=')):
            self.process_motor_encoder_velocity(driver_board_id, message[6:])
        elif (message[4:].startswith('T=')):
            self.process_motor_temperature(driver_board_id, message[6:])
        elif (message[4:].startswith('V=')):
            self.process_motor_driver_board_power_voltage(driver_board_id, message[6:])
        elif (message[4:].startswith('CR=')):
            self.process_motor_encoder_position_count_relative(driver_board_id, message[7:])
        elif (message[4:].startswith('FF=')):
            self.process_motor_driver_board_status(driver_board_id, message[7:])
        else:
            print(message)

    def process_GPS_message(self, message: AnyStr) -> None:
        print(message)

    def close_connection(self):
        self.client_socket.close()

    def process_motor_current(self, driver_board_id: int, param: AnyStr) -> None:
        values = param.split(":")
        p = ""
        if driver_board_id == 0:
            p = "front"
        elif driver_board_id == 1:
            p = "rear"
        print("Motor current left {0} = {1}".format(p, values[0]))
        print("Motor current right {0} = {1}".format(p, values[1]))

    def process_motor_temperature(self, driver_board_id: int, param: AnyStr) -> None:
        values = param.split(":")
        p = ""
        if driver_board_id == 0:
            p = "front"
        elif driver_board_id == 1:
            p = "rear"
        print("Motor temperature left {0} = {1}".format(p, values[0]))
        print("Motor temperature right {0} = {1}".format(p, values[1]))

    def process_motor_encoder_position_count(self, driver_board_id: int, param: AnyStr) -> None:
        values = param.split(":")
        p = ""
        if driver_board_id == 0:
            p = "front"
        elif driver_board_id == 1:
            p = "rear"
        print("Encoder position count left {0} = {1}".format(p, values[0]))
        print("Encoder position count right {0} = {1}".format(p, values[1]))

    def process_motor_encoder_position_count_relative(self, driver_board_id: int, param: AnyStr) -> None:
        values = param.split(":")
        p = ""
        if driver_board_id == 0:
            p = "front"
        elif driver_board_id == 1:
            p = "rear"
        print("Encoder position count relative left {0} = {1}".format(p, values[0]))
        print("Encoder position count relative right {0} = {1}".format(p, values[1]))

    def process_motor_output_power(self, driver_board_id: int, param: AnyStr) -> None:
        # motor output power (PWM) -1000~ 1000
        values = param.split(":")
        p = ""
        if driver_board_id == 0:
            p = "front"
        elif driver_board_id == 1:
            p = "rear"
        print("Motor output power left {0} = {1}".format(p, values[0]))
        print("Motor output power right {0} = {1}".format(p, values[1]))

    def process_motor_encoder_velocity(self, driver_board_id: int, param: AnyStr) -> None:
        values = param.split(":")
        p = ""
        if driver_board_id == 0:
            p = "front"
        elif driver_board_id == 1:
            p = "rear"
        print("Encoder velocity  {0} = {1} RPM".format(p, values[0]))
        print("Encoder velocity  {0} = {1} RPM".format(p, values[1]))

    def process_motor_driver_board_power_voltage(self, driver_board_id: int, param: AnyStr) -> None:
        values = param.split(":")
        p = ""
        if driver_board_id == 0:
            p = "front"
        elif driver_board_id == 1:
            p = "rear"
        print("Motor driver board power 12V {0} = {1} V".format(p, int(values[0]) / 10.0))
        print("Motor driver board power Main {0} = {1} V".format(p, int(values[1]) / 10.0))
        print("Motor driver board power 5V {0} = {1} V".format(p, int(values[2]) / 1000.0))

    def process_motor_driver_board_status(self, driver_board_id: int, value: AnyStr) -> None:
        pass
        flags = int(value)
        overheat = flags & 1 > 0
        overvoltage = flags & 2 > 0
        undervoltage = flags & 4 > 0
        short_circuit = flags & 8 > 0
        emergency_stop = flags & 16 > 0
        brushless_sensor_fault  = flags & 32 > 0
        mosfet_failure = flags & 64 > 0
        custom_flag = flags & 64 > 0

        if driver_board_id == 0:
            p = "front"
        elif driver_board_id == 1:
            p = "rear"
        print("Motor driver board status {0} overheat = {1}".format(p, overheat))
        print("Motor driver board status {0} overvoltage = {1}".format(p, overvoltage))
        print("Motor driver board status {0} undervoltage = {1}".format(p, undervoltage))
        print("Motor driver board status {0} short_circuit = {1}".format(p, short_circuit))
        print("Motor driver board status {0} emergency_stop = {1}".format(p, emergency_stop))
        print("Motor driver board status {0} brushless_sensor_fault = {1}".format(p, brushless_sensor_fault))
        print("Motor driver board status {0} mosfet_failure = {1}".format(p, mosfet_failure))
        print("Motor driver board status {0} custom_flag = {1}".format(p, custom_flag))


def test_read_sensors():
    test = TestReadSensors()

    test.test_read()


if __name__ == '__main__':
    test_read_sensors()
