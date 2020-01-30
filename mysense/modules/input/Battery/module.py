from core.modules import InputModule
from core.config_file import ConfigFile
from core.log import *

class Battery(InputModule):
    """
    Reading battery voltage using an analog digital converter.
    """

    def __init__(self):
        super(Battery, self).__init__()
        from modules.platform.LoPy4.module import LoPy4Battery
        self.bat = LoPy4Battery(self.config().get("pin"))

    def get_id():
        return 7

    def get(self):
        ret = bytearray(1)
        ret[0] = int(self.bat.voltage() * 10)
        log_debug("Battery: " + str(ret[0]))
        return ret

    def decode(array):
        s = "\t\"Battery\":\n\t{\n"
        s += "\t\t\"level\": " + str(array[0] / 10) + "\n"
        s += "\t}"
        return s

    def test(self):
        self.get()

    def get_config_definition():
        return (
            "input_battery",
            "Reads the battery using an ADC.",
            (
                ("pin", "17", "Defines the pin to read the voltage from.", ConfigFile.VariableType.uint),
            )
        )
