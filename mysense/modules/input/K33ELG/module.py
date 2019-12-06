from core.modules import InputModule
from core.config_file import ConfigFile

class K33ELG(InputModule):
    """
    A simple date/time input module.
    """

    def __init__(self):
        super(K33ELG, self).__init__()
        from modules.input.K33ELG.dep.k33elg import K33ELG as K33ELG_drv
        self.__sensor = K33ELG_drv(self.config().get("pin_sda"), self.config().get("pin_scl"))

    def get_id():
        return 6

    def get(self):
        return InputModule.uint16_to_bytearray(self.__sensor.get_value())

    def decode(array):
        s = "\t\"KG33ELG\":\n\t{\n"
        s += "\t\t\"co2\": " + str(InputModule.bytearray_to_uint16(array, 0)) + "\n"
        s += "\t}"
        return s

    def test(self):
        pass

    def get_config_definition():
        return (
            "input_kg33egl",
            "Adds support for the Senseair K33ELG sensor.",
            (
                ("pin_sda", "20", "Defines the sda pin.", ConfigFile.VariableType.uint),
                ("pin_scl", "21", "Defines the scl pin.", ConfigFile.VariableType.uint),
            )
        )
