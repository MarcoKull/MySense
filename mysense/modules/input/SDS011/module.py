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
from core.devices import UART_Device
from core.log import *

class SDS011(InputModule, UART_Device):
    """
    Import module for the PMSx003 fine particular sensor.
    """

    def __init__(self):
        InputModule.__init__(self)
        UART_Device.__init__(self, "SDS011")
        from modules.input.SDS011.dep.SDS011 import SDS011 as SDS011_drv
        self.sensor = SDS011_drv(port=self.uart_port(), pins=("P" + str(self.config().get("pin_rx")), "P" + str(self.config().get("pin_tx"))))

    def get_id():
        return 10

    def get(self):
        try:
            data = self.sensor.getData()
            return InputModule.concat_bytearrays(
                (
                    InputModule.uint16_to_bytearray(data[0][1]*10),
                    InputModule.uint16_to_bytearray(data[1][1]*10),
                )
            )
        except:
            b = bytearray(20)
            for i in range(0, len(b)):
                b[i] = 0
            return b

    def decode(array):
        s = "\t\"SDS011\":\n\t{\n"
        s += "\t\t\"pm25\": " + str(InputModule.bytearray_to_uint16(array, 0) / 10) + ",\n"
        s += "\t\t\"pm10\": " + str(InputModule.bytearray_to_uint16(array, 2) / 10) + ",\n"
        s += "\t}"
        return s

    def test(self):
        pass

    def get_config_definition():
        return (
            "SDS011",
            "Support for the SDS011 fine particle sensor.",
            (
                ("pin_rx", "3", "Defines RX pin.", ConfigFile.VariableType.uint),
                ("pin_tx", "4", "Defines TX pin.", ConfigFile.VariableType.uint),
            )
        )
