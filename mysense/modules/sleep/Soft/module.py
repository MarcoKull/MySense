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

try:
    import time # python
except:
    import utime as time # micropython

class Soft(SleepModule):
    """
    This is a simple sleep class to be used as reference.
    It should only be used for testing because it does not make use of any power saving.
    """

    def __init__(self):
        super(Soft, self).__init__()
        self.seconds = self.config().get("seconds")

    def get_config_definition():
        return (
            "sleep_soft",
            "This module uses the standart utime library to sleep.\nAs it does not use any power management functions it should only be used for testing.",
            (
                ("seconds", "3", "Defines how many seconds to sleep.", ConfigFile.VariableType.uint),
            )
        )

    def sleep(self):
        log_info("Using software sleep to sleep " + str(self.seconds) + " seconds.")
        # sleep only one second at a time
        # this not just for printing but also possibly for feeding a watchdog timer
        for i in range(self.seconds, 0, -1):
            log_all("Software sleep for " + str(i) + " seconds.")
            time.sleep(1)


    def test(self):
        pass
