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
from core.log import *

class Battery(InputModule):
    """
    Reading battery voltage using an analog digital converter.
    """

    def __init__(self):
        super(Battery, self).__init__()
        from modules.platform.LoPy4.module import LoPy4Battery
        self.bat = LoPy4Battery(self.config().get("pin"))

    def get_id():
        return 7

    def get(self):
        ret = bytearray(1)
        ret[0] = int(self.bat.voltage() * 10)
        log_debug("Battery: " + str(ret[0]))
        return ret

    def decode(array):
        s = "\t\"Battery\":\n\t{\n"
        s += "\t\t\"level\": " + str(array[0] / 10) + "\n"
        s += "\t}"
        return s

    def test(self):
        self.get()

    def get_config_definition():
        return (
            "input_battery",
            "Reads the battery using an ADC.",
            (
                ("pin", "17", "Defines the pin to read the voltage from.", ConfigFile.VariableType.uint),
            )
        )
