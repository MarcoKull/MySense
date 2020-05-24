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

from machine import UART
from time import sleep, sleep_ms
import utime
from core.log import *

class SDS011:
    def __init__(self, port=1, debug=False, numSample = 30, wait=20, pins = ('P3', 'P4')):
        self.numSample = numSample
        self.uart = UART(port, 9600)                         # init with given baudrate
        self.uart.init(9600, bits=8, parity=None, stop=1, pins=pins) # init with given parameters

        self.starttime = utime.ticks_ms() + (wait*1000)

    def checkChecksum(self,inputRaw):
        checksum = 0
        for i in range(2,8):
            checksum = (checksum + inputRaw[i]) & 0xff

        if(checksum == inputRaw[8]): # Test checksum
            return True
        else:
            return False

    def fillFields(self,inputRaw): #Calculate PM2.5 and PM10 values using formula datasheet
        self.SDS011_Fields[0][2] = inputRaw[3]*256 + inputRaw[2]/10
        self.SDS011_Fields[1][2] = inputRaw[5]*256 + inputRaw[4]/10

    def average(self): #Calculate moving average
        self.SDS011_Fields[2][1] = self.SDS011_Fields[2][1] + 1
        self.SDS011_Fields[0][1] = (((1/self.SDS011_Fields[2][1])*self.SDS011_Fields[0][2])+(((self.SDS011_Fields[2][1]-1)/self.SDS011_Fields[2][1])*self.SDS011_Fields[0][1]))
        self.SDS011_Fields[1][1] = (((1/self.SDS011_Fields[2][1])*self.SDS011_Fields[1][2])+(((self.SDS011_Fields[2][1]-1)/self.SDS011_Fields[2][1])*self.SDS011_Fields[1][1]))
        

    def sample(self):
        for i in range(self.numSample):
            sleep(1)
            if self.uart.any():
                data_raw=self.uart.read()
                if(self.checkChecksum(data_raw)):
                    self.fillFields(data_raw)
                    self.average()
                    log_debug(str(self.SDS011_Fields))
                    
    def readyToSample(self):
        now = utime.ticks_ms()
        if now > self.starttime:
            pass
        else:
            log_debug("Waiting for sampling SDS011")
            sleep_ms(self.starttime-now)
        
    def getData(self): #Sample for 60 seconds check checksum and calculate moving average.
        self.SDS011_Fields = [
            ['PM25', 0, 0],
            ['PM10', 0, 0],
            ['n', 0]
        ]
        self.readyToSample()
        self.sample() #Try to sample 60 times
        return self.SDS011_Fields