# This file is part of the MySense software (https://github.com/MarcoKull/MySense).
# Copyright (c) 2020 
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

try:
  from micropython import const
  from time import ticks_ms, sleep_ms, sleep
except:
  try:
    from const import const, ticks_ms, sleep_ms
  except:
    from time import time
    def sleep_ms(ms): sleep(ms/1000.0)
    def ticks_ms(): return int(time()*1000)
    def const(a): return a

import struct         # needed for unpack data telegram
def ORD(val):
  if type(val) is str:
    return ord(val) & 0xFF
  return val & 0xFF

""" Get sensor values from sensirion SPS30
"""

class SPS30:
  # index of list
  START_MEASURING = bytearray(b'\x7E\x00\x00\x02\x01\x03\xF9\x7E')
  READ_MEASUREMENT = bytearray(b'\x7E\x00\x03\x00\xFC\x7E')
  FAN_CLEANING = bytearray(b'\x7E\x00\x56\x00\xA9\x7E')
  STOP_MEASUREMENT = bytearray(b'\x7E\x00\x01\x00\xFE\x7E')
  PM_fields = [
      ['pm1','ug/m3',0,0],
      ['pm25','ug/m3',0,0],
      ['pm4','ug/m3',0,0],
      ['pm10','ug/m3',0,0],
 
      ['pm05_cnt','pcs/cm3',0,None],
      ['pm1_cnt','pcs/cm3',0,None],
      ['pm25_cnt','pcs/cm3',0,None],
      ['pm4_cnt','pcs/cm3',0,None],
      ['pm10_cnt','pcs/cm3',0,None],
      ['typ_par','um',0,None],
    ]
  
  pm1_pos = const(0)
  pm25_pos = const(1)
  pm4_pos = const(2)
  pm10_pos = const(3)
  pm05_cnt_pos = const(4)
  pm1_cnt_pos = const(5)
  pm25_cnt_pos = const(6)
  pm4_cnt_pos = const(7)
  pm10_cnt_pos = const(8)
  typ_par_pos = const(9)

  # idle time minimal time to switch fan OFF
  IDLE  = const(120000)   # minimal idle time between sample time and interval
  def __init__(self, port=1, debug=False, sample=60, interval=1200, raw=False, calibrate=None,pins=('P3','P4'), clean=None, explicit=False):

    try:
      if type(port) is str: # no PyCom case
        import serial
        self.ser = serial.Serial(port, 115200, bytesize=8, parity='N', stopbits=1, timeout=20, xonxoff=0, rtscts=0)
        self.ser.any = self.in_waiting
      elif type(port) is int: # micro python case
        from machine import UART
        self.ser = UART(port,baudrate=115200,pins=pins,timeout_chars=10)
      else: self.ser = port # fd
    except: raise OSError("PMS serial failed")

    self.firmware = None
    self.debug = debug
    self.interval = interval * 1000 # if interval == 0 no auto fan switching
    self.sample =  sample *1000
    self.raw = raw
    self.explicit = explicit        # counts are > PM size or < PM size

    # list of name, units, index in measurments, calibration factoring
    # pm1=[20,1] adds a calibration offset of 20 to measurement
    self.PM_fields = [
      # concentration (generic atmosphere conditions) in ug/m3
      ['pm1','ug/m3',0,0],
      ['pm25','ug/m3',0,0],
      ['pm4','ug/m3',0,0],
      ['pm10','ug/m3',0,0],
 
      ['pm05_cnt','pcs/cm3',0,None],
      ['pm1_cnt','pcs/cm3',0,None],
      ['pm25_cnt','pcs/cm3',0,None],
      ['pm4_cnt','pcs/cm3',0,None],
      ['pm10_cnt','pcs/cm3',0,None],
      ['typ_par','um',0,None],
    ]

  def StartMeasuring(self):
    self.ser.write(self.START_MEASURING)
    sleep_ms(100)
    self.ser.read()
    return True

  def unpack_measurements(self,inputbyte):
    output = [None]*10
    inputstart = 5
    for i in range(10):
        var = inputbyte[inputstart:inputstart+4]
        output[i]=struct.unpack('>f',var)
        inputstart = inputstart+4
    return output

  def destuff(self,inputbyte):
    output = [0]*47
    cnt = 0
    if len(inputbyte) > 47:
      i=0
      while i < len(inputbyte):
        if(inputbyte[i]==125):
          if(inputbyte[i+1] == 94):
            output[cnt] = 126
            cnt = cnt+1

          elif(inputbyte[i+1] == 93):
            output[cnt] = 125
            cnt = cnt+1

          elif(inputbyte[i+1] == 49):
            output[cnt] =  17
            cnt = cnt+1

          elif(inputbyte[i+1] == 51):
            output[cnt] = 19
            cnt = cnt+1           

          i = i+2

        else:
          output[cnt]=inputbyte[i]
          cnt = cnt+1
          i = i+1

        
    else:
        output=inputbyte

    return output

  def getData(self,debug=False):
    self.StartMeasuring()
    sleep_ms(5000)

    self.ser.write(self.READ_MEASUREMENT)
    sleep_ms(500)

    if self.ser.any():
      newMeasurement = self.ser.read()
      newMeasurement_destuffed = self.destuff(newMeasurement)
      unpacked = self.unpack_measurements(bytes(newMeasurement_destuffed))
      #print(unpacked)

      for i in range(len(self.PM_fields)):
        self.PM_fields[i][2] = unpacked[i][0]

    return self.PM_fields


if __name__ == "__main__":
  import sys
  from time import time, sleep
  interval = 5*60
  sample = 60
  debug = True
  explicit = False   # True: Plantower way of count, False: Sensirion way (dflt=False)
  SPS30 = SPS30(debug=debug, sample=sample, interval=interval, explicit=explicit)
  for i in range(100):
    lastTime = time()
    print(SPS30.getData(debug=debug))
    sleep(2)