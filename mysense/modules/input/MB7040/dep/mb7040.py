from core.devices import I2C_Device
import time


class MB7040(I2C_Device):
    """Driver for the """

    def __init__(self, pin_sda, pin_scl):
        I2C_Device.__init__(self, "MB7040", 0x70, pin_sda, pin_scl)

    def measure(self):
        # initialize a write
        self.write(224)

        # write range command
        self.write(81)

        # wait for sensor to measure
        time.sleep_ms(80)

        # initialize a read
        self.write(225)

        # get measurement
        m = self.read(2)

        return m[1] + (m[0] << 8)
