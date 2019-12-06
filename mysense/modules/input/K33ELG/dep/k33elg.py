# based on https://github.com/kimata/rasp-python/blob/master/lib/sensor/k30.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# K30 を使って CO2 濃度を取得するライブラリです．
#
# 作成時に使用したのは，SenseAir の
#「CO2 Engine 30」．
# http://senseair.se/products/oem-modules/k30/

from core.devices import I2C_Device
import utime as time

class K33ELG(I2C_Device):
    NAME                = 'K30'

    DEV_ADDR		= 0x68 # 7bit

    RAM_CO2		= 0x08
    RAM_FIRM		= 0x62

    WRITE_RAM		= 0x1 << 4
    READ_RAM		= 0x2 << 4
    WRITE_EE		= 0x3 << 4
    READ_EE		= 0x4 << 4

    RETRY_COUNT         = 5

    def __init__(self, pin_sda, pin_scl):
        I2C_Device.__init__(self, "K33ELG", K33ELG.DEV_ADDR, pin_sda, pin_scl)

    def ping(self):
        for i in range(self.RETRY_COUNT):
            try:
                return True
                time.sleep(0.2)
            except:
                pass

        return False

    def ping_impl(self):
    #    try:
        command = [ self.READ_RAM|0x1, 0x00, self.RAM_FIRM ]
        command = self.__compose_command(command)

        #self.i2cbus.write(self.dev_addr, command)
        self.write(bytearray(command))

        time.sleep(0.5)

        #value = self.i2cbus.read(self.DEV_ADDR, 3)
        val = bytearray(3)
        self.readinto(val)

        time.sleep(0.15)

    #        return True
    #    except:
    #        return False

    def __compose_command(self, command):
        return command + [sum(command) & 0xFF]

    def get_value(self):
        error = None
        for i in range(self.RETRY_COUNT):
            try:
                self.ping()
                return self.get_value_impl()
            except Exception as e:
                error = e
                time.sleep(0.15)
        raise error

    def get_value_impl(self):
        command = [ self.READ_RAM|0x2, 0x00, self.RAM_CO2 ]
        command = self.__compose_command(command)

        #self.i2cbus.write(self.dev_addr, command)
        self.write(bytearray(command))

        time.sleep(0.15)

        #value = self.i2cbus.read(self.DEV_ADDR, 4)
        value = bytearray(4)
        self.readinto(value)
        print(self.i2c.readfrom_mem(, reg, 1)[0])
        time.sleep(0.15)

        if (list(bytearray(value))[0] & 0x1) != 0x1:
            raise Exception('command incomplete')

        if list(bytearray(value)) != \
           self.__compose_command(list(bytearray(value))[0:3]):
            raise Exception('invalid sum')

        import struct
        co2 = struct.unpack('>H', bytes(value[1:3]))[0]
        print(co2)
        return co2

    def get_value_map(self):
        value = self.get_value()

        return { 'co2': value[0] }

if __name__ == '__main__':
    # TEST Code
    import pprint
    import sensor.k30
    I2C_BUS = 0x1 # I2C のバス番号 (Raspberry Pi は 0x1)

    k30 = sensor.k30.K30(I2C_BUS)

    ping = k30.ping()
    print('PING: %s' % ping)

    if (ping):
        pprint.pprint(k30.get_value_map())


##!/usr/bin/env python
## -*- coding: utf-8 -*-
#
## K30 を使って CO2 濃度を取得するライブラリです．
##
## 作成時に使用したのは，SenseAir の
##「CO2 Engine 30」．
## http://senseair.se/products/oem-modules/k30/
#
#import time
#import struct
#import sys
#import traceback
#
#if __name__ == '__main__':
#    import os
#    import sys
#    sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
#
#import i2cbus
#
#class K30:
#    NAME                = 'K30'
#
#    DEV_ADDR		= 0x68 # 7bit
#
#    RAM_CO2		= 0x08
#    RAM_FIRM		= 0x62
#
#    WRITE_RAM		= 0x1 << 4
#    READ_RAM		= 0x2 << 4
#    WRITE_EE		= 0x3 << 4
#    READ_EE		= 0x4 << 4
#
#    RETRY_COUNT         = 5
#
#    def __init__(self, bus, dev_addr=DEV_ADDR):
#        self.bus = bus
#        self.dev_addr = dev_addr
#        self.i2cbus = i2cbus.I2CBus(bus)
#
#    def ping(self):
#        for i in range(self.RETRY_COUNT):
#            if self.ping_impl():
#                return True
#            time.sleep(0.2)
#        return False
#
#    def ping_impl(self):
#        try:
#            command = [ self.READ_RAM|0x1, 0x00, self.RAM_FIRM ]
#            command = self.__compose_command(command)
#
#            self.i2cbus.write(self.dev_addr, command)
#
#            time.sleep(0.15)
#
#            value = self.i2cbus.read(self.DEV_ADDR, 3)
#
#            time.sleep(0.15)
#
#            return True
#        except:
#            return False
#
#    def __compose_command(self, command):
#        return command + [sum(command) & 0xFF]
#
#    def get_value(self):
#        error = None
#        for i in range(self.RETRY_COUNT):
#            try:
#                return self.get_value_impl()
#            except Exception as e:
#                error = e
#                time.sleep(0.15)
#        raise error
#
#    def get_value_impl(self):
#        command = [ self.READ_RAM|0x2, 0x00, self.RAM_CO2 ]
#        command = self.__compose_command(command)
#
#        self.i2cbus.write(self.dev_addr, command)
#
#        time.sleep(0.15)
#
#        value = self.i2cbus.read(self.DEV_ADDR, 4)
#
#        time.sleep(0.15)
#
#        if (list(bytearray(value))[0] & 0x1) != 0x1:
#            raise Exception('command incomplete')
#
#        if list(bytearray(value)) != \
#           self.__compose_command(list(bytearray(value))[0:3]):
#            raise Exception('invalid sum')
#
#        co2 = struct.unpack('>H', bytes(value[1:3]))[0]
#        return [ co2 ]
#
#    def get_value_map(self):
#        value = self.get_value()
#
#        return { 'co2': value[0] }
#
#if __name__ == '__main__':
#    # TEST Code
#    import pprint
#    import sensor.k30
#    I2C_BUS = 0x1 # I2C のバス番号 (Raspberry Pi は 0x1)
#
#    k30 = sensor.k30.K30(I2C_BUS)
#
#    ping = k30.ping()
#    print('PING: %s' % ping)
#
#    if (ping):
#        pprint.pprint(k30.get_value_map())
#
