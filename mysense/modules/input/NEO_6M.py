from core.modules import InputModule
from core.config_file import ConfigFile

class NEO_6M(InputModule):
    """
    Input module for the NEO-6M GPS sensor.
    """

    def __init__(self):
        super(NEO_6M, self).__init__()
        from drivers.gps_dexter import GROVEGPS
        self.sensor = GROVEGPS()

    def get_id():
        return 0

    def get(self):
        data = self.sensor.MyGPS()

        return InputModule.concat_bytearrays(
            (
                InputModule.uint32_to_bytearray(data[0] * 10000),
                InputModule.uint32_to_bytearray(data[1] * 10000),
                InputModule.uint16_to_bytearray(data[2])
            )
        )

    def decode(array):
        s = "\t\"NEO-6M\":\n\t{\n"
        s += "\t\t\"latitude\": " + str(InputModule.bytearray_to_uint32(array, 0) / 10000) + ",\n"
        s += "\t\t\"longitude\": " + str(InputModule.bytearray_to_uint32(array, 4) / 10000) + ",\n"
        s += "\t\t\"altitude\": " + str(InputModule.bytearray_to_uint16(array, 8)) + "\n"
        s += "\t}"
        return s

    def test(self):
        pass

    def get_config_definition():
        return None