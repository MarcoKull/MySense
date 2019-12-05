from core.modules import InputModule
from core.config_file import ConfigFile

class BME680(InputModule):
    """
    A input module for the Bosch BME680 sensor.
    """

    def __init__(self):
        super(BME680, self).__init__()
        from drivers.bme680 import BME680 as BME680_drv
        self.sensor = BME680_drv(self.config().get("pin_sda"), self.config().get("pin_scl"))

    def get_id():
        return 3

    def get(self):
        return InputModule.concat_bytearrays(
            (
                InputModule.uint16_to_bytearray((self.sensor.temperature + 100) * 100),
                InputModule.uint16_to_bytearray(self.sensor.humidity * 100),
                InputModule.uint32_to_bytearray(self.sensor.pressure * 100),
                InputModule.uint16_to_bytearray(self.sensor.altitude * 100),
                InputModule.uint32_to_bytearray(self.sensor.gas)
            )
        )

    def decode(array):
        t = InputModule.bytearray_to_uint16(array, 0) / 100 -100
        h = InputModule.bytearray_to_uint16(array, 2) / 100
        p = InputModule.bytearray_to_uint32(array, 4) / 100
        a = InputModule.bytearray_to_uint16(array, 8) / 100
        g = InputModule.bytearray_to_uint32(array, 10)

        s = "\t\"BME680\":\n\t{\n"
        s += "\t\t\"temperature\": " + str(t) + ",\n"
        s += "\t\t\"humidity\": " + str(h) + ",\n"
        s += "\t\t\"pressure\": " + str(p) + ",\n"
        s += "\t\t\"altitude\": " + str(a) + ",\n"
        s += "\t\t\"gas\": " + str(g) + "\n"
        s += "\t}"
        return s

    def test(self):
        self.get()

    def get_config_definition():
        return (
            "input_bme680",
            "Adds support for the Bosch BME680 sensor.\nIt measures humidity, gas, altitude, temperature and airpressure.",
            (
                ("pin_sda", "20", "Defines the sda pin.", ConfigFile.VariableType.uint),
                ("pin_scl", "21", "Defines the scl pin.", ConfigFile.VariableType.uint),
            )
        )
