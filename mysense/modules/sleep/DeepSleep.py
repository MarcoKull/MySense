from modules.sleep_module import SleepModule
from core.config_file import ConfigFile
from log.log import *



class DeepSleep(SleepModule):
    """
    This sleep class makes use of the deep sleep functionalty of the LoPy4.
    """

    def __init__(self):

        # load config file
        conf = ConfigFile(
            "config/sleep_deepsleep.conf",
            (
                ("seconds", "3", "Defines how many seconds to sleep.", ConfigFile.VariableType.uint),
            )
        )

        self.seconds = conf.get("seconds")

    def sleep(self):
        log_info("Using deep sleep to sleep " + str(self.seconds) + " seconds.")
        import machine
        machine.deepsleep(self.seconds * 1000)

    def get_config_definition():
        return (
            "sleep_deepsleep",
            "This module uses the LoPy4's deep sleep feature.\nNotice while this makes use of power saving after the sleep time the device will boot again.",
            (
                ("seconds", "3", "Defines how many seconds to sleep.", ConfigFile.VariableType.uint),
            )
        )
