from core.devices import I2C_Device
import utime as time
import struct
from machine import Pin

class K33ELG(I2C_Device):

    def __init__(self, pin_sda, pin_scl):
        # now that the device woke up initialize i2c bus
        I2C_Device.__init__(self, "K33ELG", 0x68, pin_sda, pin_scl)

        # create pins to send wake up condition
        self.__sda = Pin('P' + str(pin_sda), mode=Pin.OUT)
        self.__scl = Pin('P' + str(pin_scl), mode=Pin.OUT)

        # last measurement
        self.__last = 0

    def __command(self, arg0, arg1):
        tries = 5
        for t in range(0, tries):
            try:
                # wake up
                self.__wake()

                # write command
                self.write(bytearray([0x22, 0x00, arg0, arg1]))

                # wait for device to deliver values
                time.sleep_ms(20)

                # read values from sensor
                buf = self.read(4)

                # check sum to see if we have a valid response
                sum = 0
                for i in range(0, len(buf) - 1):
                    sum += buf[i]

                if sum % 256 != buf[len(buf) - 1]:
                    raise Exception("checksum error")

                val = 0
                val |= buf[1] & 0xFF
                val = val << 8
                val |= buf[2] & 0xFF

                return val

            except Exception as e:
                if t == tries - 1:
                    raise e
                time.sleep_ms(20)

    def __wake(self):
        # wake up sequence
        self.__scl.value(1)
        self.__sda.value(1)
        time.sleep_ms(1)
        self.__sda.value(0)
        time.sleep_ms(1)

    def __measure(self):
        # only measure once a second
        if time.ticks_ms() - self.__last > 1000:
            tries = 5
            for t in range(0, tries):
                try:
                    self.__wake()
                    self.write(bytearray([0x11, 0x00, 0x60, 0x35,0xA6]))
                    time.sleep_ms(20)
                    val=self.read(2)

                    # wait until co2 value arrives
                    while self.__read_co2() == 0:
                        time.sleep(0.5)

                    self.__last = time.ticks_ms()
                    return

                except Exception as e:
                    if t == tries - 1:
                        raise e
                    time.sleep_ms(20)

    def __read_co2(self):
        return self.__command(0x08, 0x2A)

    def __read_humidity(self):
        return self.__command(0x14, 0x36) / 100

    def __read_temperature(self):
        return self.__command(0x12, 0x34) / 100

    def get_co2(self):
        self.__measure()
        return self.__read_co2()

    def get_humidity(self):
        self.__measure()
        return self.__read_humidity()

    def get_temperature(self):
        self.__measure()
        return self.__read_temperature()
