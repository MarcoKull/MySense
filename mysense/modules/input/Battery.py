from core.modules import InputModule
from core.config_file import ConfigFile

class Battery(InputModule):
    """
    Reading battery voltage using an analog digital converter.
    The output is between 0 (empty) and 255 (fully charged).
    """

    def __init__(self):
        super(Battery, self).__init__()

        from machine import ADC
        adc = ADC()
        self.bat = adc.channel(pin="P" + str(self.config().get("pin")), attn=ADC.ATTN_11DB)

    def get_id():
        return 7

    def __get(self):
        return int(self.bat.value() / 4095 * 255)

    def get(self):
        # get 10 samples
        values = []
        for i in range(0, 10):
            values.append(self.__get())
        values.sort()

        # take the median
        ret = bytearray(1)
        ret[0] = values[int(len(values) / 2)]
        return ret

    def decode(array):
        s = "\t\"Battery\":\n\t{\n"
        s += "\t\t\"level\": " + str(array[0]) + "\n"
        s += "\t}"
        return s

    def test(self):
        self.get()

    def get_config_definition():
        return (
            "input_battery",
            "Reads the battery using an ADC. Outputs a value between 0 and 255.",
            (
                ("pin", "17", "Defines the pin to read the voltage from.", ConfigFile.VariableType.uint),
            )
        )
