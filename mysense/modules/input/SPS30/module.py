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

class SPS30(InputModule, UART_Device):
    """
    Import module for the PMSx003 fine particular sensor.
    """

    def __init__(self):
        InputModule.__init__(self)
        UART_Device.__init__(self, "SPS30")
        from modules.input.SPS30.dep.SPS30 import SPS30 as SPS30_drv
        self.sensor = SPS30_drv(port=self.uart_port(), pins=("P" + str(self.config().get("pin_rx")), "P" + str(self.config().get("pin_tx"))))

    def get_id():
        return 9

    def get(self):
        try:
            data = self.sensor.getData()
            print(data)
            return InputModule.concat_bytearrays(
                (
                    InputModule.uint16_to_bytearray(int(data[0][2]*10)),
                    InputModule.uint16_to_bytearray(int(data[1][2]*10)),
                    InputModule.uint16_to_bytearray(int(data[2][2]*10)),
                    InputModule.uint16_to_bytearray(int(data[3][2]*10)),
                    InputModule.uint16_to_bytearray(int(data[4][2]*10)),
                    InputModule.uint16_to_bytearray(int(data[5][2]*10)),
                    InputModule.uint16_to_bytearray(int(data[6][2]*10)),
                    InputModule.uint16_to_bytearray(int(data[7][2]*10)),
                    InputModule.uint16_to_bytearray(int(data[8][2]*10)),
                    InputModule.uint16_to_bytearray(int(data[9][2]*10))
                )
            )
        except:
            b = bytearray(20)
            for i in range(0, len(b)):
                b[i] = 0
            return b

    def decode(array):
        s = "\t\"SPS30\":\n\t{\n"
        s += "\t\t\"pm1\": " + str(InputModule.bytearray_to_uint16(array, 0) / 10) + ",\n"
        s += "\t\t\"pm25\": " + str(InputModule.bytearray_to_uint16(array, 2) / 10) + ",\n"
        s += "\t\t\"pm4\": " + str(InputModule.bytearray_to_uint16(array, 4) / 10) + ",\n"
        s += "\t\t\"pm10\": " + str(InputModule.bytearray_to_uint16(array, 6) / 10) + ",\n"
        s += "\t\t\"pm05_cnt\": " + str(InputModule.bytearray_to_uint16(array, 8) / 10) + ",\n"
        s += "\t\t\"pm1_cnt\": " + str(InputModule.bytearray_to_uint16(array, 10) / 10) + ",\n"
        s += "\t\t\"pm25_cnt\": " + str(InputModule.bytearray_to_uint16(array, 12) / 10) + ",\n"
        s += "\t\t\"pm4_cnt\": " + str(InputModule.bytearray_to_uint16(array, 14) / 10) + ",\n"
        s += "\t\t\"pm10_cnt\": " + str(InputModule.bytearray_to_uint16(array, 16) / 10) + ",\n"
        s += "\t\t\"typ_par\": " + str(InputModule.bytearray_to_uint16(array, 18) / 10) + ",\n"
        s += "\t}"
        return s

    def test(self):
        pass

    def get_config_definition():
        return (
            "SPS30",
            "Support for the SPS30 fine particle sensor.",
            (
                ("pin_rx", "3", "Defines RX pin.", ConfigFile.VariableType.uint),
                ("pin_tx", "4", "Defines TX pin.", ConfigFile.VariableType.uint),
            )
        )
