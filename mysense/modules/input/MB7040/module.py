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

class MB7040(InputModule):
    """
    A input module for the Bosch BME680 sensor.
    """
    def __init__(self):
        super(MB7040, self).__init__()
        from modules.input.MB7040.dep.mb7040 import MB7040 as MB7040_drv
        self.sensor = MB7040_drv(self.config().get("pin_sda"), self.config().get("pin_scl"))

    def get_id():
        return 8

    def get(self):
        return InputModule.uint16_to_bytearray(self.sensor.measure())

    def decode(array):
        s = "\t\"MB7040\":\n\t{\n"
        s += "\t\t\"distance_cm\": " + str(InputModule.bytearray_to_uint16(array, 0)) + "\n\t}"
        return s

    def test(self):
        self.get()

    def get_config_definition():
        return (
            "input_mb7040",
            "Adds support for the MB7040 I2C distance sensor.",
            (
                ("pin_sda", "20", "Defines the sda pin.", ConfigFile.VariableType.uint),
                ("pin_scl", "21", "Defines the scl pin.", ConfigFile.VariableType.uint),
            )
        )
