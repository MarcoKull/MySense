from core.modules import InputModule
from core.config_file import ConfigFile

import utime

class PMSx003(InputModule):
    """
    Import module for the PMSx003 fine particular sensor.
    """

    def __init__(self):
        super(PMSx003, self).__init__()
        from drivers.pmsx003 import PMSx003 as PMSx003_drv
        self.sensor = PMSx003_drv(pins=("P" + str(self.config().get("pin_rx")), "P" + str(self.config().get("pin_tx"))))

    def get_id():
        return 4

    def get(self):
        data = self.sensor.getData()

        return InputModule.concat_bytearrays(
            (
                InputModule.uint16_to_bytearray(data["pm1_par1"] * 100),
                InputModule.uint16_to_bytearray(data["pm25_par2"] * 100),
                InputModule.uint16_to_bytearray(data["pm10_par3"] * 100),
                InputModule.uint16_to_bytearray(data["pm1"] * 100),
                InputModule.uint16_to_bytearray(data["pm25"] * 100),
                InputModule.uint16_to_bytearray(data["pm10"] * 100),
                InputModule.uint16_to_bytearray(data["pm05_cnt"] * 100),
                InputModule.uint16_to_bytearray(data["pm1_cnt"] * 100),
                InputModule.uint16_to_bytearray(data["pm25_cnt"] * 100),
                InputModule.uint16_to_bytearray(data["pm5_cnt"] * 100),
                InputModule.uint16_to_bytearray(data["pm10_cnt"] * 100),
                InputModule.uint16_to_bytearray(data["grain"] * 100)
            )
        )

    def decode(array):
        s = "\t\"PMSx003\":\n\t{\n"
        s += "\t\t\"pm1_par1\": " + str(InputModule.bytearray_to_uint16(array, 0) / 100) + ",\n"
        s += "\t\t\"pm25_par2\": " + str(InputModule.bytearray_to_uint16(array, 2) / 100) + ",\n"
        s += "\t\t\"pm10_par3\": " + str(InputModule.bytearray_to_uint16(array, 4) / 100) + ",\n"
        s += "\t\t\"pm1\": " + str(InputModule.bytearray_to_uint16(array, 6) / 100) + ",\n"
        s += "\t\t\"pm25\": " + str(InputModule.bytearray_to_uint16(array, 8) / 100) + ",\n"
        s += "\t\t\"pm10\": " + str(InputModule.bytearray_to_uint16(array, 10) / 100) + ",\n"
        s += "\t\t\"pm05_cnt\": " + str(InputModule.bytearray_to_uint16(array, 12) / 100) + ",\n"
        s += "\t\t\"pm1_cnt\": " + str(InputModule.bytearray_to_uint16(array, 14) / 100) + ",\n"
        s += "\t\t\"pm25_cnt\": " + str(InputModule.bytearray_to_uint16(array, 16) / 100) + ",\n"
        s += "\t\t\"pm5_cnt\": " + str(InputModule.bytearray_to_uint16(array, 18) / 100) + ",\n"
        s += "\t\t\"pm10_cnt\": " + str(InputModule.bytearray_to_uint16(array, 20) / 100) + ",\n"
        s += "\t\t\"grain\": " + str(InputModule.bytearray_to_uint16(array, 22) / 100) + "\n"
        s += "\t}"
        return s

    def test(self):
        pass

    def get_config_definition():
        return (
            "input_pmsx003",
            "Support for the PMSx003 fine particle sensor.",
            (
                ("pin_rx", "3", "Defines RX pin.", ConfigFile.VariableType.uint),
                ("pin_tx", "4", "Defines TX pin.", ConfigFile.VariableType.uint),
            )
        )
