# This file is part of the MySense software (https://github.com/MarcoKull/MySense).
# Copyright (c) 2020 Jelle Adema
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

# Give in the percentage away from sensor and adapt lights.
from modules.status.DistanceIndicator.dep.ws2812 import WS2812
from array import array
from machine import Pin

class distanceLightClass(WS2812):
    def __init__(self, ledNumber=1,brightness=100):
        WS2812.__init__(self, ledNumber=1,brightness=100)
        self.ledNumber = ledNumber
        self.ledArray = [(255,165,0)] * self.ledNumber
        p_out = Pin('P9', mode=Pin.OUT)
        p_out.value(1)
        self.show(self.ledArray)

    def standby(self):

        ledArray = [(0,0,0)] * self.ledNumber

        for i in range((self.ledNumber//2)-5,(self.ledNumber//2)+5,1):
            ledArray[i] = (255,165,0)
        print(ledArray)

        self.show(ledArray)

    def percentageLight(self, percentClose = 100):

        ledArray = [(255,0,0)] * self.ledNumber

        greenLeds = ((100 - percentClose) / 100) * self.ledNumber
        halveGreenLeds = int(greenLeds/2)

        middleLed = self.ledNumber // 2

        for i in range(middleLed-halveGreenLeds,middleLed+halveGreenLeds,1):
            ledArray[i] = (0,255,0)

        self.show(ledArray)
