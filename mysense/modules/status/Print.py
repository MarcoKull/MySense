from modules.status_module import StatusModule
from log.log_level import LogLevel
from log.logger import Logger

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

    def set_status(self, type):
        msg = "Switched to '" + str(type) + "' mode."
        Logger().log(self.level, msg)

    def test(self):
        pass
