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

try:
    import time # python
except:
    import utime as time # micropython

class DateTime(InputModule):
    """
    A simple date/time input module.
    """

    def __init__(self):
        super(DateTime, self).__init__()

    def get_id():
        return 0

    def get(self):
        t = time.localtime() # get time

        array = bytearray(6)
        array[0] = t[0] - 1970
        array[1] = t[1]
        array[2] = t[2]
        array[3] = t[3]
        array[4] = t[4]
        array[5] = t[5]

        return array

    def decode(array):
        s = "\t\"DateTime\":\n\t{\n"
        s += "\t\t\"year\": " + str(array[0] + 1970) + ",\n"
        s += "\t\t\"month\": " + str(array[1]) + ",\n"
        s += "\t\t\"day\": " + str(array[2]) + ",\n"
        s += "\t\t\"hour\": " + str(array[3]) + ",\n"
        s += "\t\t\"minute\": " + str(array[4]) + ",\n"
        s += "\t\t\"second\": " + str(array[5]) + "\n\t}"
        return s

    def test(self):
        self.get()

    def get_config_definition():
        return None
