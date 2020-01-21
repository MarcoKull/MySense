from core.modules import InputModule
from core.config_file import ConfigFile

class MB7040(InputModule):
    """
    A input module for the Bosch BME680 sensor.
    """
    def __init__(self):
        super(MB7040, self).__init__()
        from modules.input.MB7040.dep.mb7040 import MB7040 as MB7040_drv
        self.sensor = MB7040_drv(self.config().get("pin_sda"), self.config().get("pin_scl"))

    def get_id():
        return 8

    def get(self):
        return InputModule.uint16_to_bytearray(self.sensor.measure())

    def decode(array):
        s = "\t\"MB7040\":\n\t{\n"
        s += "\t\t\"distance_cm\": " + str(InputModule.bytearray_to_uint16(array, 0)) + "\n\t}"
        return s

    def test(self):
        self.get()

    def get_config_definition():
        return (
            "input_mb7040",
            "Adds support for the MB7040 I2C distance sensor.",
            (
                ("pin_sda", "20", "Defines the sda pin.", ConfigFile.VariableType.uint),
                ("pin_scl", "21", "Defines the scl pin.", ConfigFile.VariableType.uint),
            )
        )
