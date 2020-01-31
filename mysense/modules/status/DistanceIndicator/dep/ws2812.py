# -*- coding: utf-8 -*-
# Based on https://github.com/JanBednarik/micropython-ws2812
# Adapted for LoPy by @aureleq

import gc
from machine import SPI
from machine import Pin
from machine import disable_irq
from machine import enable_irq
from uos import uname

class WS2812:
    """
    Driver for WS2812 RGB LEDs. May be used for controlling single LED or chain
    of LEDs.

    Example of use:

        chain = WS2812(ledNumber=4)
        data = [
            (255, 0, 0),    # red
            (0, 255, 0),    # green
            (0, 0, 255),    # blue
            (85, 85, 85),   # white
        ]
        chain.show(data)

    Version: 1.0
    """
    # Values to put inside SPI register for each color's bit
    buf_bytes = (b'\xE0\xE0', # 0  0b00
                 b'\xE0\xFC', # 1  0b01
                 b'\xFC\xE0', # 2  0b10
                 b'\xFC\xFC') # 3  0b11

    def __init__(self, ledNumber=1, brightness=100):
        """
        Params:
        * ledNumber = count of LEDs
        * brightness = light brightness (integer : 0 to 100%)
        """
        self.ledNumber = ledNumber
        self.brightness = brightness

        # Prepare SPI data buffer (8 bytes for each color)
        self.buf_length = self.ledNumber * 3 * 8
        self.buf = bytearray(self.buf_length)

        # SPI init
        # Bus 0, 8MHz => 125 ns by bit, 8 clock cycle when bit transfert+2 clock cycle between each transfert
        # => 125*10=1.25 us required by WS2812
        self.spi = SPI(0, SPI.MASTER, baudrate=8000000, polarity=0, phase=1)
        
        # Turn LEDs off
        self.show([])

    def show(self, data):
        """
        Show RGB data on LEDs. Expected data = [(R, G, B), ...] where R, G and B
        are intensities of colors in range from 0 to 255. One RGB tuple for each
        LED. Count of tuples may be less than count of connected LEDs.
        """
        self.fill_buf(data)
        self.send_buf()

    def send_buf(self):
        """
        Send buffer over SPI.
        """
        disable_irq()
        self.spi.write(self.buf)
        enable_irq()
        gc.collect()

    def update_buf(self, data, start=0):
        """
        Fill a part of the buffer with RGB data.

        Order of colors in buffer is changed from RGB to GRB because WS2812 LED
        has GRB order of colors. Each color is represented by 4 bytes in buffer
        (1 byte for each 2 bits).

        Returns the index of the first unfilled LED

        Note: If you find this function ugly, it's because speed optimisations
        beated purity of code.
        """

        buf = self.buf
        buf_bytes = self.buf_bytes
        brightness = self.brightness

        index = start * 24
        for red, green, blue in data:
            red = int(red * brightness // 100)
            green = int(green * brightness // 100)
            blue = int(blue * brightness // 100)

            buf[index:index+2] = buf_bytes[green >> 6 & 0b11]
            buf[index+2:index+4] = buf_bytes[green >> 4 & 0b11]
            buf[index+4:index+6] = buf_bytes[green >> 2 & 0b11]
            buf[index+6:index+8] = buf_bytes[green & 0b11]

            buf[index+8:index+10] = buf_bytes[red >> 6 & 0b11]
            buf[index+10:index+12] = buf_bytes[red >> 4 & 0b11]
            buf[index+12:index+14] = buf_bytes[red >> 2 & 0b11]
            buf[index+14:index+16] = buf_bytes[red & 0b11]

            buf[index+16:index+18] = buf_bytes[blue >> 6 & 0b11]
            buf[index+18:index+20] = buf_bytes[blue >> 4 & 0b11]
            buf[index+20:index+22] = buf_bytes[blue >> 2 & 0b11]
            buf[index+22:index+24] = buf_bytes[blue & 0b11]

            index += 24

        return index // 24

    def fill_buf(self, data):
        """
        Fill buffer with RGB data.

        All LEDs after the data are turned off.
        """
        end = self.update_buf(data)

        # Turn off the rest of the LEDs
        buf = self.buf
        off = self.buf_bytes[0]
        for index in range(end * 24, self.buf_length):
            buf[index:index+2] = off
            index += 2
            
    def set_brightness(self, brightness):
        """
        Set brighness of all leds
        """
        self.brightness = brightness

