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

from core.modules import OutputModule

from core.log import *

class Print(OutputModule):
    """
    Example of an output module that prints the output to the log.
    """
    def __init__(self):
        super(Print, self).__init__()
        self.level = LogLevel.debug

    def get_log_level(self):
        return self.level

    def set_log_level(self, level):
        self.level = level

    log_level = property(get_log_level, set_log_level)

    def send(self, binary, base64, json, json_base64):
        s = "Output: sizes - binary(" + str(len(binary)) + ") base64(" + str(len(base64)) + ") json(" + str(len(json)) + ") json_base64(" + str(len(json_base64)) + ")\n"
        s += " BASE64: " + base64 + "\n"
        s += " JSON BASE64: " + json_base64 + "\n"
        s += " JSON:\n" + json
        log(self.level, s)

    def test(self):
        pass

    def get_config_definition():
        return None
