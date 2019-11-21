from core.modules import OutputModule

from core.log import *

class Print(OutputModule):
    """
    Example of an output module that prints the output to the log.
    """
    def __init__(self):
        super(Print, self).__init__()
        self.level = LogLevel.debug

    def get_log_level(self):
        return self.level

    def set_log_level(self, level):
        self.level = level

    log_level = property(get_log_level, set_log_level)

    def send(self, binary, base64, json):
        s = "Output: sizes - binary(" + str(len(binary)) + ") base64(" + str(len(base64)) + ") json(" + str(len(json)) + ")\n"
        s += " BASE64: " + base64 + "\n"
        s += " JSON:\n" + json
        log(self.level, s)

    def test(self):
        pass

    def get_config_definition():
        return None
