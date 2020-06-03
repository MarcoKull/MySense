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

from core.modules import InputModule
from core.config_file import ConfigFile
from modules.input.StevalMKI158.dep.stevalMKI158 import StevalMKI158 as stevalMKI158_drv
from core.log import *

class StevalMKI158(InputModule):
    """
    A input module for the Bosch BME680 sensor.
    """

    def __init__(self):
        super(StevalMKI158, self).__init__()
        
        self.sensor = stevalMKI158_drv()

    def get_id():
        return 25

    def get(self):
        return InputModule.concat_bytearrays(
            (
                InputModule.uint16_to_bytearray(self.sensor.get_x_acceleration()),
                InputModule.uint16_to_bytearray(self.sensor.get_y_acceleration()),
                InputModule.uint16_to_bytearray(self.sensor.get_z_acceleration()),
            )
        )

    def decode(array):
        x = InputModule.bytearray_to_uint16(array, 0)
        y = InputModule.bytearray_to_uint16(array, 2)
        z = InputModule.bytearray_to_uint16(array, 4)
        s = "\t\"StevalMKI158\":\n\t{\n"
        s += "\t\t\"X\": " + str(x) + ",\n"
        s += "\t\t\"Y\": " + str(y) + ",\n"
        s += "\t\t\"Z\": " + str(z) + ",\n"
        return s

    def test(self):
        pass

    def get_config_definition():
        return (
            "input_stevalMKI158",
            "Adds support for the LeddarOne sensor.\nIt measures distance using infrared light.",
            (
                ("pin_sda", "9", "Defines the sda pin.", ConfigFile.VariableType.uint),
                ("pin_scl", "10", "Defines the scl pin.", ConfigFile.VariableType.uint),
            )
        )
