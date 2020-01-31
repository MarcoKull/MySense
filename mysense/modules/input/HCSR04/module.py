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

class HCSR04(InputModule):
    """
    Distance measuring using the HC-SR04 sensor.
    """

    def __init__(self):
        super(HCSR04, self).__init__()
        from modules.input.HCSR04.dep.hcsr04 import HCSR04 as HCSR04_drv
        self.sensor = HCSR04_drv(self.config().get("pin_echo"), self.config().get("pin_trigger"), self.config().get("samples"))

    def get_id():
        return 1

    def get(self):
        return InputModule.uint16_to_bytearray(self.sensor.measure())

    def decode(array):
        s = "\t\"HCSR04\":\n\t{\n"
        s += "\t\t\"distance_cm\": " + str(InputModule.bytearray_to_uint16(array, 0)) + "\n\t}"
        return s

    def test(self):
        self.get()

    def get_config_definition():
        return (
            "input_hcsr04",
            "Adds support for the HCSR04 distance sensor.",
            (
                ("pin_echo", "20", "Defines the echo pin.", ConfigFile.VariableType.uint),
                ("pin_trigger", "21", "Defines the trigger pin.", ConfigFile.VariableType.uint),
                ("samples", "20", "Defines how many samples should be taken.", ConfigFile.VariableType.uint),
            )
        )
