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

class K33ELG(InputModule):
    """
    A simple date/time input module.
    """

    def __init__(self):
        super(K33ELG, self).__init__()
        from modules.input.K33ELG.dep.k33elg import K33ELG as K33ELG_drv
        self.__sensor = K33ELG_drv(self.config().get("pin_sda"), self.config().get("pin_scl"))

    def get_id():
        return 6

    def get(self):
        return InputModule.concat_bytearrays(
            (
                InputModule.uint16_to_bytearray((self.__sensor.get_temperature() + 100) * 100),
                InputModule.uint16_to_bytearray(self.__sensor.get_humidity() * 100),
                InputModule.uint16_to_bytearray(self.__sensor.get_co2())
            )
        )

    def decode(array):
        s = "\t\"KG33ELG\":\n\t{\n"
        s += "\t\t\"temperature\": " + str(InputModule.bytearray_to_uint16(array, 0) / 100 - 100) + ",\n"
        s += "\t\t\"humidity\": " + str(InputModule.bytearray_to_uint16(array, 2) / 100) + ",\n"
        s += "\t\t\"co2\": " + str(InputModule.bytearray_to_uint16(array, 4)) + "\n"
        s += "\t}"
        return s

    def test(self):
        pass

    def get_config_definition():
        return (
            "input_kg33egl",
            "Adds support for the Senseair K33ELG sensor.",
            (
                ("pin_sda", "20", "Defines the sda pin.", ConfigFile.VariableType.uint),
                ("pin_scl", "21", "Defines the scl pin.", ConfigFile.VariableType.uint),
            )
        )
