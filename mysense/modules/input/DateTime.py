from modules.input_module import InputModule
from core.config_file import ConfigFile

import utime

class DateTime(InputModule):
    """
    A simple date/time input module.
    """

    def __init__(self):
        super(DateTime, self).__init__()

    def get_id():
        return 0

    def get(self):
        t = utime.localtime() # get time

        array = bytearray(6)
        array[0] = t[0] - 1970
        array[1] = t[1]
        array[2] = t[2]
        array[3] = t[3]
        array[4] = t[4]
        array[5] = t[5]

        return array

    def decode(array):
        s = "\t\"DateTime\":\n\t{\n"
        s += "\t\t\"year\": " + str(array[0] + 1970) + ",\n"
        s += "\t\t\"month\": " + str(array[1]) + ",\n"
        s += "\t\t\"day\": " + str(array[2]) + ",\n"
        s += "\t\t\"hour\": " + str(array[3]) + ",\n"
        s += "\t\t\"minute\": " + str(array[4]) + ",\n"
        s += "\t\t\"second\": " + str(array[5]) + "\n\t}"
        return s

    def test(self):
        pass

    def get_config_definition():
        return None
