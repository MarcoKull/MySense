from machine import I2C
import time

class StevalMKI153():
    def __init__(self, pins=('P9','P10'), baudrate=115200):
        self.i2c = I2C(0, I2C.MASTER, pins=pins)
        self.i2c.init(I2C.MASTER, baudrate=baudrate)
        self.i2c.writeto_mem(0x19, 0x20, 0x47) #need to write this to turn power mode to normal

    def twos_complement(self, value, bits):
        """compute the 2's complement of int value val"""
        if (value & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            value = value - (1 << bits)        # compute negative value
        return value                         # return positive value as is

    def calculate_measurement(self, high_byte, low_byte):
        """all the calculation required: converting the high and low bits to 1 number, then getting twos complement"""
        x = low_byte | high_byte << 8
        x = twos_complement(x, len(bin(int(str(x), 10)).lstrip('0b')))
        x = x * 1000 / 2047
        return x
    
    def get_x_acceleration(self):
        if self.i2c.scan():
            #### Reading X axis
            buf = bytearray(1)
            self.i2c.readfrom_mem_into(0x19, 0x28, buf)
            low_bits_x = int.from_bytes(buf, 'big', True)
            self.i2c.readfrom_mem_into(0x19, 0x29, buf)
            high_bits_x = int.from_bytes(buf, 'big', True)
            acceleration_x = self.calculate_measurement(high_bits_x, low_bits_x)
            #print("x axis " + str(acceleration_x))
            return acceleration_x

    def get_y_acceleration(self):
        if self.i2c.scan():
            #### Reading X axis
            buf = bytearray(1)
            self.i2c.readfrom_mem_into(0x19, 0x2A, buf)
            low_bits_y = int.from_bytes(buf, 'big', True)
            self.i2c.readfrom_mem_into(0x19, 0x2B, buf)
            high_bits_y = int.from_bytes(buf, 'big', True)
            acceleration_y = self.calculate_measurement(high_bits_y, low_bits_y)
            #print("y axis " + str(acceleration_y))
            return acceleration_y

    def get_z_acceleration(self):
        if self.i2c.scan():
            #### Reading X axis
            buf = bytearray(1)
            self.i2c.readfrom_mem_into(0x19, 0x2C, buf)
            low_bits_z = int.from_bytes(buf, 'big', True)
            self.i2c.readfrom_mem_into(0x19, 0x2D, buf)
            high_bits_z = int.from_bytes(buf, 'big', True)
            acceleration_z = self.calculate_measurement(high_bits_z, low_bits_z)
            #print("z axis " + str(acceleration_z))
            return acceleration_z
