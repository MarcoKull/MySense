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

class StatusLED(StatusModule):
    """
    Status indicator using the built-in LoPy4 LED as status indicator.
    """

    def __init__(self):
        from modules.status.StatusLED.dep.lopy4_led import LoPy4LED
        self.led = LoPy4LED()

    def status(self, type):
        from modules.status.StatusLED.dep.lopy4_led import LoPy4LED
        if type == StatusModule.StatusType.error:
            self.led.set_color(LoPy4LED.Color.red)

        if type == StatusModule.StatusType.booting:
            self.led.set_color(LoPy4LED.Color.white)

        if type == StatusModule.StatusType.testing:
            self.led.set_color(LoPy4LED.Color.orange)

        if type == StatusModule.StatusType.measuring:
            self.led.set_color(LoPy4LED.Color.yellow)

        if type == StatusModule.StatusType.sending:
            self.led.set_color(LoPy4LED.Color.green)

        if type == StatusModule.StatusType.ota:
            self.led.set_color(LoPy4LED.Color.blue)

        if type == StatusModule.StatusType.sleeping:
            self.led.set_color(LoPy4LED.Color.purple)

    def log(self, level, message):
        pass

    def measurement(self, bytearray, json):
        pass

    def test(self):
        pass

    def get_config_definition():
        return None
