from modules.module import Module
from log.log_observer import LogObserver

class StatusModule(Module, LogObserver):
    """
    Abstract class for status modules.
    The status(type) method has to implemented by the child class.
    """

    def __init__(self):
        pass

    def status(self, type):
        raise NotImplementedError("The status(type) method has to implemented by a StatusModule child class.")

    def measurement(self, json):
        raise NotImplementedError("The measurement(json) method has to implemented by a StatusModule child class.")

    class StatusType():
        error = "error"
        booting = "booting"
        testing = "testing"
        measuring = "measuring"
        sending = "sending"
        sleeping = "sleeping"
        ota = "ota"
