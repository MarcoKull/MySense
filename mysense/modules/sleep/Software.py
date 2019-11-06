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

        # load config file
        conf = ConfigFile(
            "config/sleep_software.conf",
            (
                ("seconds", "3", "This module should only be used for testing.\n\nDefines how many seconds to sleep.", ConfigFile.VariableType.uint),
            )
        )

        self.seconds = conf.get("seconds")

    def sleep(self):
        log_info("Using software sleep to sleep " + str(self.seconds) + " seconds.")
        utime.sleep(self.seconds)
