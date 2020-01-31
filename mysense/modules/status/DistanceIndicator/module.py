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

class DistanceIndicator(StatusModule):
    """
    A status indicator that prints the current state in the log.
    """
    def __init__(self):
        from modules.status.DistanceIndicator.dep.distanceLight import distanceLightClass
        self._light = distanceLightClass(ledNumber=60,brightness=100)
        self._light.percentageLight(100)

    def status(self, type):
        #log_info("YEAH!")
        pass

    def test(self):
        pass

    def measurement(self, array, json):
        d = array[1] + (array[0] << 8)

        min = 15
        max = 200

        if d < min:
            p = 100
        elif d > max:
            p = 0
        else:
            p = 100 - ((d - min) / (max - min) * 100)

        self._light.percentageLight(p)

    def get_config_definition():
        return None

    def log(self, level, message):
        pass
