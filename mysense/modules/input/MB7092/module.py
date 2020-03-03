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

class MB7092(InputModule):
    """
    Distance measuring using the MaxSonar MB7092 sensor.
    """

    def __init__(self):
        super(MB7092, self).__init__()
        from modules.input.MB7092.dep.mb7092 import MB7092 as MB7092_drv
        self.sensor = MB7092_drv(self.config().get("pin_tx"), self.config().get("pin_am"), self.config().get("samples"))

    def get_id():
        return 2

    def get(self):
        return InputModule.uint16_to_bytearray(self.sensor.measure())

    def decode(array):
        s = "\t\"MB7092\":\n\t{\n"
        s += "\t\t\"distance_cm\": " + str(InputModule.bytearray_to_uint16(array, 0)) + "\n\t}"
        return s

    def test(self):
        self.get()

    def get_config_definition():
        return (
            "input_mb7092",
            "distance mb7092",
            (
                ("pin_tx", "20", "Defines the tx pin (pin 4).", ConfigFile.VariableType.uint),
                ("pin_am", "16", "Defines the am pin (pin 3).", ConfigFile.VariableType.uint),
                ("samples", "20", "Defines how many samples should be taken.", ConfigFile.VariableType.uint),
            )
        )
