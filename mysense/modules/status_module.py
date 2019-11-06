from modules.module import Module

class StatusModule(Module):
    """
    Abstract class for status modules.
    The set_status(type) method has to implemented by the child class.
    """

    def __init__(self):
        pass

    def set_status(self, type):
        raise NotImplementedError("The set_status(type) method has to implemented by the child class.")


    class StatusType():
        error = "error"
        booting = "booting"
        testing = "testing"
        measuring = "measuring"
        sending = "sending"
        sleeping = "sleeping"
        ota = "ota"
