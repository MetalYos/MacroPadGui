import serial

class SerialPort:
    def __init__(self, port, baudrate=115200, timeout=0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None

    def open(self):
        if self.serial is not None:
            return True

        try:
            self.serial = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
            return True
        except serial.SerialException as e:
            print(f'SerialPort::open: {e}')
            return False

    def close(self):
        if self.serial is None:
            return

        self.serial.close()
        self.serial = None

    def is_open(self):
        if self.serial is None:
            return False

        return self.serial.is_open

    def read(self, size):
        if self.serial is None:
            return None

        return self.serial.read(size)

    def write(self, data):
        if self.serial is None:
            return 0

        return self.serial.write(data)
