from modules.module import Module

class PlatformModule(Module):
    """
        Abstract class for platform modules.
        The is_run_tests() and ota_update(path) method has to implemented by the child class.
    """

    def __init__(self):
        super(PlatformModule, self).__init__()
        pass

    def is_run_tests(self):
        raise NotImplementedError("The is_run_tests() method has to implemented by a PlatformModule child class.")

    def ota_update(self, path):
        raise NotImplementedError("The ota_update(path) method has to implemented by a PlatformModule child class.")
