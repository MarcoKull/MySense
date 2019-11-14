from modules.platform_module import PlatformModule

class LoPy4(PlatformModule):
    """
    This class wrapps the generic LoPy4 features.
    The goal is to keep the core class independent from pycom libraries.
    """

    def __init__(self):
        import pycom
        # disable blue flashing of the led
        pycom.heartbeat(False)

    def is_run_tests(self):
        # TODO: only test on hard reset
        return True

    def test(self):
        pass

    def get_config_definition():
        return None
