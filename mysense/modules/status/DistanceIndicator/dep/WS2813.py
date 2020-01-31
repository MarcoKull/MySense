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
        