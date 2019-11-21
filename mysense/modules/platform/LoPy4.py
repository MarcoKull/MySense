from core.modules import PlatformModule

class LoPy4(PlatformModule):
    """
    This class wrapps the generic LoPy4 features.
    The goal is to keep the core class independent from pycom libraries.
    """

    def __init__(self):
        pass

    def is_run_tests(self):
        # only run test if not woke up from deep sleep
        import machine
        return machine.reset_cause() != machine.DEEPSLEEP_RESET

    def test(self):
        pass

    def get_config_definition():
        return None
