from modules.input_module import InputModule
from core.config_file import ConfigFile

class HCSR04(InputModule):
    """
    Distance measuring using the HC-SR04 sensor.
    """

    def __init__(self):
        super(HCSR04, self).__init__()
        from drivers.hcsr04 import HCSR04 as HCSR04_drv
        self.sensor = HCSR04_drv(self.config().get("pin_echo"), self.config().get("pin_trigger"))

    def get_id():
        return 1

    def get(self):
        # get the measurement
        d = self.sensor.measure()

        # transform it to 2 bytes
        arr = bytearray(2)
        arr[0] = (d >> 8) & 0xff
        arr[1] = d & 0xff

        return arr

    def decode(array):
        d = array[1] + (array[0] << 8)

        s = "\t\"HCSR04\":\n\t{\n"
        s += "\t\t\"distance_cm\": " + str(d) + "\n\t}"
        return s

    def test(self):
        pass

    def get_config_definition():
        return (
            "input_hcsr04",
            "distance hcsr04",
            (
                ("pin_echo", "20", "Defines the echo pin.", ConfigFile.VariableType.uint),
                ("pin_trigger", "21", "Defines the trigger pin.", ConfigFile.VariableType.uint),
            )
        )
