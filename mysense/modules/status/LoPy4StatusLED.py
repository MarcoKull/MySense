from modules.status_module import StatusModule
from drivers.lopy4_led import LoPy4LED

class LoPy4StatusLED(StatusModule):
    """
    Status indicator using the built-in LoPy4 LED as status indicator.
    """

    def __init__(self):
        self.led = LoPy4LED()

    def set_status(self, type):
        if type == StatusModule.StatusType.error:
            self.led.set_color(LoPy4LED.Color.red)

        if type == StatusModule.StatusType.booting:
            self.led.set_color(LoPy4LED.Color.white)

        if type == StatusModule.StatusType.testing:
            self.led.set_color(LoPy4LED.Color.orange)

        if type == StatusModule.StatusType.measuring:
            self.led.set_color(LoPy4LED.Color.yellow)

        if type == StatusModule.StatusType.sending:
            self.led.set_color(LoPy4LED.Color.green)

        if type == StatusModule.StatusType.ota:
            self.led.set_color(LoPy4LED.Color.blue)

        if type == StatusModule.StatusType.sleeping:
            self.led.set_color(LoPy4LED.Color.purple)

    def test(self):
        pass
