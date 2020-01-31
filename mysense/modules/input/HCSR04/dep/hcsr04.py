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

import machine
from machine import Pin

import utime

class HCSR04():
    """
    Driver for the Ultrasonic HC-SR04 sensor.
    Most code was taken from https://core-electronics.com.au/tutorials/hc-sr04-ultrasonic-sensor-with-pycom-tutorial.html
    and https://github.com/andrey-git/micropython-hcsr04/blob/master/hcsr04.py
    """

    def __init__(self, pin_echo, pin_trigger, samples):
        self.echo = Pin('P' + str(pin_echo), mode=Pin.IN)
        self.trigger = Pin('P' + str(pin_trigger), mode=Pin.OUT)
        self.__samples = samples
        self.trigger(0)

    def __measure_once(self):
        # Stabilize the sensor
        self.trigger(0)
        utime.sleep_us(2)

        # Send a 10us pulse.
        self.trigger(1)
        utime.sleep_us(10)
        self.trigger(0)

        # wait for the rising edge of the echo then start timer
        start = utime.ticks_us()
        while self.echo() == 0:
            if utime.ticks_us() - start > 1000000:
                raise Exception("Timeout starting HCSR04 distance sensor.")
            pass
        start = utime.ticks_us()

        # wait for end of echo pulse then stop timer
        while self.echo() == 1:
            # timeout after one second
            if utime.ticks_us() - start > 1000000:
                raise Exception("Timeout reading HCSR04 distance sensor.")

        finish = utime.ticks_us()

        # pause for 20ms to prevent overlapping echos
        utime.sleep_ms(20)

        # calculate distance by using time difference between start and stop
        # speed of sound 340m/s or .034cm/us. Time * .034cm/us = Distance sound travelled there and back
        # divide by two for distance to object detected.

        return int(((utime.ticks_diff(start, finish)) * .034)/-2)

        return distance

    def __median(self, array):
        sort = sorted(array)
        return array[int(len(array)/2)]

    def measure(self):
        samples = []

        for j in range(self.__samples):
            try:
                samples.append(self.__measure_once())
            except:
                samples.append(self.__measure_once())

        return self.__median(samples)

    def get_distance():
        return 0
