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

from machine import Pin
from machine import ADC
import utime

class MB7092():
    """Driver for the MaxSonar MB7092 distance sensor."""

    def __init__(self, pin_rx, pin_am, samples):
        super(MB7092, self).__init__()

        # pin to enable/disable measurement
        self.rx = Pin('P' + str(pin_rx), mode=Pin.OUT)
        self.rx(1)
        self.__samples = samples
        # setting up the Analog/Digital Converter with 10 bits
        adc = ADC()

        # create an analog pin on P16 for the ultrasonic sensor
        self.am = adc.channel(pin='P' + str(pin_am))

    def measure(self):
        samples = []
    	for j in range(self.__samples):
            try:
                samples.append(self.__measure_once())
            except:
                samples.append(self.__measure_once())

        return self.__median(samples)

    def __measure_once(self):
        self.rx(1)

        # wait for sensor to settle
        utime.sleep_us(20)

        # read distance
        d = self.am.voltage() / 4.9

        # disable measuring
        self.rx(0)

        return int(d)
    
    def __median(self, array):
        sort = sorted(array)
        return array[int(len(array)/2)]
