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
