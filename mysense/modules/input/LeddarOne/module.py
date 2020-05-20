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
from modules.input.LeddarOne.dep.LeddarOne import LeddarOne as LeddarOneSensor

class LeddarOne(InputModule):
    """
    A input module for the Bosch BME680 sensor.
    """

    def __init__(self):
        super(LeddarOne, self).__init__()
        
        self.sensor = LeddarOneSensor()

    def get_id():
        return 22

    def get(self):
        array = bytearray(1)
        return InputModule.uint16_to_bytearray(self.sensor.read_input_registers())

    def decode(array):
        t = InputModule.bytearray_to_uint16(array, 0)
        s = "\t\"LeddarOne\":\n\t{\n"
        s += "\t\t\"Distance\": " + str(t) + ",\n"
        return s

    def test(self):
        pass

    def get_config_definition():
        return (
            "input_leddarone",
            "Adds support for the LeddarOne sensor.\nIt measures distance using infrared light.",
            (
                ("pin_sda", "3", "Defines the sda pin.", ConfigFile.VariableType.uint),
                ("pin_scl", "4", "Defines the scl pin.", ConfigFile.VariableType.uint),
            )
        )
