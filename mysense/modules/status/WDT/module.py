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
from core.config_file import ConfigFile
from core.log import *

class WDT(StatusModule):
    """
    A status modue that uses the invocation of the status functions to feed a watchdog timer.
    """
    def __init__(self):
        super(WDT, self).__init__()
        from machine import WDT as PYCOM_WDT
        self.wdt = PYCOM_WDT(timeout=1000*self.config().get("timeout"))

    def feed(self):
        self.wdt.feed()

    def status(self, type):
        self.feed()

    def log(self, level, message):
        self.feed()

    def test(self):
        self.feed()

    def measurement(self, bytearray, json):
        self.feed()

    def get_config_definition():
        return (
            "status_wdt",
            "This module is a watchdog using the status functions as a way too be fed.",
            (
                ("timeout", "60", "Defines how many seconds to wait after the last status message occured until the device is reset.", ConfigFile.VariableType.uint),
            )
        )
