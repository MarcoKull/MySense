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

from core.modules import SleepModule
from core.config_file import ConfigFile
from core.log import *



class Deep(SleepModule):
    """
    This sleep class makes use of the deep sleep functionalty of the LoPy4.
    """

    def __init__(self):
        super(Deep, self).__init__()
        self.seconds = self.config().get("seconds")

    def sleep(self):
        log_info("Using deep sleep to sleep " + str(self.seconds) + " seconds.")
        import machine
        machine.deepsleep(self.seconds * 1000)

    def get_config_definition():
        return (
            "sleep_deep",
            "This module uses the LoPy4's deep sleep feature.\nNotice while this makes use of power saving after the sleep time the device will boot again.",
            (
                ("seconds", "3", "Defines how many seconds to sleep.", ConfigFile.VariableType.uint),
            )
        )

    def test(self):
        pass
