# This file is part of the MySense software (https://github.com/MarcoKull/MySense).
# Copyright (c) 2020 Marco Kull
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from core.log import *

class I2C_Device(object):
    """
    Handles devices that connect to an I2C bus.
    """

    __counter = 0
    __busses = dict()

    def __init__(self, name, address, pin_sda, pin_scl):
        from machine import I2C, Pin

        self.address = address

        if (pin_sda, pin_scl) not in I2C_Device.__busses.keys():
            log_debug("Initializing I2C bus " + str(I2C_Device.__counter) + " with pins sda " + str(pin_sda) + " and scl " + str(pin_scl) + ".")
            I2C_Device.__busses[(pin_sda, pin_scl)] = (I2C_Device.__counter, I2C(I2C_Device.__counter, pins=(Pin("P" + str(pin_sda)),Pin("P" + str(pin_scl)))))
            I2C_Device.__counter += 1

        # create i2c bus
        i2cbus = I2C_Device.__busses[(pin_sda, pin_scl)]
        log_debug("Initializing device '" + name + "' on I2C bus " + str(i2cbus[0]) + ".")
        self.i2c = i2cbus[1]

    def read(self, size):
        buf = bytearray(size)
        self.readinto(buf)
        return buf

    def readinto(self, buf, **kwargs):
        """
        Read into ``buf`` from the device. The number of bytes read will be the
        length of ``buf``.
        If ``start`` or ``end`` is provided, then the buffer will be sliced
        as if ``buf[start:end]``. This will not cause an allocation like
        ``buf[start:end]`` will so it saves memory.
        :param bytearray buffer: buffer to write into
        :param int start: Index to start writing at
        :param int end: Index to write up to but not include
        """
        self.i2c.readfrom_into(self.address, buf, **kwargs)

    def write(self, buf, **kwargs):
        """
        Write the bytes from ``buffer`` to the device. Transmits a stop bit if
        ``stop`` is set.
        If ``start`` or ``end`` is provided, then the buffer will be sliced
        as if ``buffer[start:end]``. This will not cause an allocation like
        ``buffer[start:end]`` will so it saves memory.
        :param bytearray buffer: buffer containing the bytes to write
        :param int start: Index to start writing from
        :param int end: Index to read up to but not include
        :param bool stop: If true, output an I2C stop condition after the buffer is written
        """
        self.i2c.writeto(self.address, buf, **kwargs)

class UART_Device(object):
    """
    Handles devices that connect to an UART bus.
    """

    __counter = 0

    def __init__(self, name):
        self.__port = UART_Device.__counter
        UART_Device.__counter += 1

        log_debug("Initializing device '" + name + "' on UART port " + str(self.__port) + ".")

    def uart_port(self):
        return self.__port
