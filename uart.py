import serial
import time

START_BYTE = 254
END_BYTE = 255


class UART_Driver:
    def __init__(self, inPort):
        # configure the serial connections (the parameters differs on the device you are connecting to)
        self.ser = serial.Serial(port=inPort, baudrate=115200)

        self.curr_v = 0
        self.curr_s = 0

    def update_velocity(
        self, new_v: int
    ):  # shifting values into UART accepted range (128-255) (zero at 191)
        if new_v < 0:
            new_v = 0
        elif new_v > 255:
            new_v = 255
        new_v = new_v >> 1

        self.curr_v = new_v

    def update_steering(
        self, new_s: int
    ):  # shifting values into UART accepted range (128-255) (zero at 191)
        if new_s <= -63:
            new_s = 0
        elif new_s >= 64:
            new_s = 127
        else:
            new_s = new_s + 64

        self.curr_s = new_s

    def reset_kart(
        self,
    ):
        self.update_velocity(0)
        self.update_steering(0)
        self.write_serial()

    def write_serial(
        self,
    ):  # the exposed keyword at the front allows the object to be accesible.

        # send start byte
        self.ser.write(START_BYTE.to_bytes(1, "little"))

        # send current velocity and steering
        self.ser.write(self.curr_v.to_bytes(1, "little"))
        self.ser.write(self.curr_s.to_bytes(1, "little"))

        # send end byte
        self.ser.write(END_BYTE.to_bytes(1, "little"))
