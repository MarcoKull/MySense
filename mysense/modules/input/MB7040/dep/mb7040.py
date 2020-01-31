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
