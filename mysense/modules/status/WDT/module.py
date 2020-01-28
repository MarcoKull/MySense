from core.modules import StatusModule
from core.config_file import ConfigFile
from core.log import *

class WDT(StatusModule):
    """
    A status modue that uses the invocation of the status functions to feed a watchdog timer.
    """
    def __init__(self):
        super(WDT, self).__init__()
        from machine import WDT as PYCOM_WDT
        self.wdt = PYCOM_WDT(timeout=1000*self.config().get("timeout"))

    def feed(self):
        self.wdt.feed()

    def status(self, type):
        self.feed()

    def log(self, level, message):
        self.feed()

    def test(self):
        self.feed()

    def measurement(self, bytearray, json):
        self.feed()

    def get_config_definition():
        return (
            "status_wdt",
            "This module is a watchdog using the status functions as a way too be fed.",
            (
                ("timeout", "60", "Defines how many seconds to wait after the last status message occured until the device is reset.", ConfigFile.VariableType.uint),
            )
        )
