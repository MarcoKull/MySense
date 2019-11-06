import pycom
import time

class LoPy4LED():
    class Color():
        blue = 0x000fff
        green = 0x007f00
        red = 0x7f0000
        white = 0xffffff
        yellow = 0x7f7f00
        orange = 0xff4500
        purple = 0x800080

    # disable heartbeat on object creation
    def __init__(self):
        pycom.heartbeat(False)

    def set_color(self, color):
        pycom.rgbled(color)
