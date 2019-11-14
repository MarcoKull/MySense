from modules.sleep_module import SleepModule
from core.config_file import ConfigFile
from log.log import *

import utime

class Software(SleepModule):
    """
    This is a simple sleep class to be used as reference.
    It should only be used for testing because it does not make use of any power saving.
    """

    def __init__(self):
        super(Software, self).__init__()
        self.seconds = self.config().get("seconds")

    def get_config_definition():
        return (
            "sleep_software",
            "This module uses the standart utime library to sleep.\nAs it does not use any power management functions it should only be used for testing.",
            (
                ("seconds", "3", "Defines how many seconds to sleep.", ConfigFile.VariableType.uint),
            )
        )

    def sleep(self):
        log_info("Using software sleep to sleep " + str(self.seconds) + " seconds.")
        utime.sleep(self.seconds)

    def test(self):
        pass
