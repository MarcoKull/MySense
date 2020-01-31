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

# Driver for WS2813
import time

class WS2813:

    def __init__(self):
        from machine import Pin #Import library

        print("Defined")
        self.p_out = Pin('P23',mode=Pin.OUT)

    def writeToLed(self, LedArray):
        for i in range(len(LedArray)):
            self.p_out.value(LedArray[i]&0b1000000)
            time.sleep_us(1)
            self.p_out.value(not(LedArray[i]&0b1000000))

            self.p_out.value(LedArray[i]&0b0100000)
            time.sleep_us(1)
            self.p_out.value(not(LedArray[i]&0b01000000))

            self.p_out.value(LedArray[i]&0b0010000)
            time.sleep_us(1)
            self.p_out.value(not(LedArray[i]&0b00100000))

            self.p_out.value(LedArray[i]&0b00010000)
            time.sleep_us(1)
            self.p_out.value(not(LedArray[i]&0b00010000))

            self.p_out.value(LedArray[i]&0b00001000)
            time.sleep_us(1)
            self.p_out.value(not(LedArray[i]&0b0001000))

            self.p_out.value(LedArray[i]&0b00000100)
            time.sleep_us(1)
            self.p_out.value(not(LedArray[i]&0b00000100))

            self.p_out.value(LedArray[i]&0b0000010)
            time.sleep_us(1)
            self.p_out.value(not(LedArray[i]&0b00000010))

            self.p_out.value(LedArray[i]&0b0000001)
            time.sleep_us(1)
            self.p_out.value(not(LedArray[i]&0b0000001))
            print(i);

        time.sleep_ms(1)
