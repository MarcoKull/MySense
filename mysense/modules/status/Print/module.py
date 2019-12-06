from core.modules import StatusModule
from core.log import *

class Print(StatusModule):
    """
    A status indicator that prints the current state in the log.
    """
    def __init__(self):

        self.level = LogLevel.debug

    def get_log_level(self):
        return self.level

    def set_log_level(self, level):
        self.level = level

    log_level = property(get_log_level, set_log_level)

    def status(self, type):
        msg = "Switched to '" + str(type) + "' mode."
        log(self.level, msg)

    def log(self, level, message):
        pass

    def test(self):
        pass

    def measurement(self, json):
        pass

    def get_config_definition():
        return None
