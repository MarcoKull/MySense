from modules.module import Module

class SleepModule(Module):
    """
        Abstract class for sleep() modules.
        The sleep() method has to implemented by the child class.
    """

    def __init__(self):
        pass

    def sleep(self):
        raise NotImplementedError("The sleep() method has to implemented by a SleepModule child class.")

    def test(self):
        pass
