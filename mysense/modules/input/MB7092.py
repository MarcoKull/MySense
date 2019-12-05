from core.modules import InputModule
from core.config_file import ConfigFile

class MB7092(InputModule):
    """
    Distance measuring using the MaxSonar MB7092 sensor.
    """

    def __init__(self):
        super(MB7092, self).__init__()
        from drivers.mb7092 import MB7092 as MB7092_drv
        self.sensor = MB7092_drv(self.config().get("pin_tx"), self.config().get("pin_am"))

    def get_id():
        return 2

    def get(self):
        return InputModule.uint16_to_bytearray(self.sensor.measure())

    def decode(array):
        s = "\t\"MB7092\":\n\t{\n"
        s += "\t\t\"distance_cm\": " + str(bytearray_to_uint16(array, 0)) + "\n\t}"
        return s

    def test(self):
        self.get()

    def get_config_definition():
        return (
            "input_mb7092",
            "distance mb7092",
            (
                ("pin_tx", "20", "Defines the tx pin (pin 4).", ConfigFile.VariableType.uint),
                ("pin_am", "16", "Defines the am pin (pin 3).", ConfigFile.VariableType.uint),
            )
        )
