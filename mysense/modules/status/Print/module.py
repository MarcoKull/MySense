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

from core.modules import StatusModule
from core.log import *

class Print(StatusModule):
    """
    A status indicator that prints the current state in the log.
    """
    def __init__(self):

        self.level = LogLevel.debug

    def get_log_level(self):
        return self.level

    def set_log_level(self, level):
        self.level = level

    log_level = property(get_log_level, set_log_level)

    def status(self, type):
        msg = "Switched to '" + str(type) + "' mode."
        log(self.level, msg)

    def log(self, level, message):
        pass

    def test(self):
        pass

    def measurement(self, bytearray, json):
        pass

    def get_config_definition():
        return None
