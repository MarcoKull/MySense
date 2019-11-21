from machine import Pin
from machine import ADC
import utime

class MB7092():
    """Driver for the MaxSonar MB7092 distance sensor."""

    def __init__(self, pin_rx, pin_am):
        super(MB7092, self).__init__()

        # pin to enable/disable measurement
        self.rx = Pin('P' + str(pin_rx), mode=Pin.OUT)
        self.rx(1)

        # setting up the Analog/Digital Converter with 10 bits
        adc = ADC()

        # create an analog pin on P16 for the ultrasonic sensor
        self.am = adc.channel(pin='P' + str(pin_am))

    def measure(self):
        # turn on measuring
        self.rx(1)

        # wait for sensor to settle
        utime.sleep_us(20)

        # read distance
        d = self.am.voltage() / 4.9

        # disable measuring
        self.rx(0)

        return int(d)
