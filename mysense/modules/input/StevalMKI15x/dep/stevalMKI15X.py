from machine import I2C
import time

class StevalMKI15X():
    def __init__(self, pins=('P9','P10'), baudrate=115200):
        self.i2c = I2C(0, I2C.MASTER, pins=pins)
        self.i2c.init(I2C.MASTER, baudrate=baudrate)

    def twos_complement(self, value, bits):
        """compute the 2's complement of int value val"""
        if (value & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            value = value - (1 << bits)        # compute negative value
        return value                         # return positive value as is

    def calculate_measurement(self, high_byte, low_byte):
        """all the calculation required: converting the high and low bits to 1 number, then getting twos complement"""
        high_bits = bin(int(str(high_byte), 10)).lstrip('0b') #convert byte value to binary
        low_bits = bin(int(str(low_byte), 10)).lstrip('0b')
        combined_bits = high_bits + '' + low_bits #concatenate bit values
        result = self.twos_complement(int(combined_bits, 2), len(combined_bits))
        result = result * 0.003 # multiply by 0.003 for +-100g (default value)
        print(result)
        result = round((result + 40) * 1000)
        result = str(result)
        return result
    
    def read_sensor(self):
        if self.i2c.scan():
            buf = bytearray(1)
            #i2c.writeto(0x19, 'abcd')
            self.i2c.writeto_mem(0x19, 0x20, 0x47)
            #### Reading X axis
            self.i2c.readfrom_mem_into(0x19, 0x28, buf)
            low_bits_x = int.from_bytes(buf, 'big', True)
            self.i2c.readfrom_mem_into(0x19, 0x29, buf)
            high_bits_x = int.from_bytes(buf, 'big', True)
            acceleration_x = self.calculate_measurement(high_bits_x, low_bits_x)
            print("x axis " + str(acceleration_x))

            #### Reading Y axis
            self.i2c.readfrom_mem_into(0x19, 0x2A, buf)
            low_bits_y = int.from_bytes(buf, 'big', True)
            self.i2c.readfrom_mem_into(0x19, 0x2B, buf)
            high_bits_y = int.from_bytes(buf, 'big', True)
            acceleration_y = self.calculate_measurement(high_bits_y, low_bits_y)
            print("y axis " + str(acceleration_y))

            #### Reading Z axis
            self.i2c.readfrom_mem_into(0x19, 0x2C, buf)
            low_bits_z = int.from_bytes(buf, 'big', True)
            self.i2c.readfrom_mem_into(0x19, 0x2D, buf)
            high_bits_z = int.from_bytes(buf, 'big', True)
            acceleration_z = self.calculate_measurement(high_bits_z, low_bits_z)
            print("z axis " + str(acceleration_z))
            return acceleration_x
