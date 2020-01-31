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
