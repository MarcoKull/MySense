from core.logger import LogObserver
from core.config_file import ConfigFile

class Module():
    """
    Abstract Module class.
    The test() ad get_config_definition() method has to implemented by the child class.
    """

    def __init__(self):
        # get config definitions
        cd = self.__class__.get_config_definition()

        # create config file
        self.__conf = self.__class__.create_config(cd)

    def test(self):
        raise NotImplementedError("The test() method has to implemented by a Module child class.")

    def get_config_definition():
        raise NotImplementedError("The get_config_definition() method has to implemented by a Module child class.")

    def create_config(config_definition):
        # module does not need a config file
        if config_definition == None:
            return None

        # create config file
        return ConfigFile(
            "config/" + config_definition[0] + ".conf",
            config_definition[1],
            config_definition[2]
        )

    def config(self):
        return self.__conf



class InputModule(Module):
    """
    Abstract class for input modules.
    The get(), get_id(), test() and decode(array) method has to implemented by the child class.
    The id has to be a unique integer.
    """

    def __init__(self):
        super(InputModule, self).__init__()

    def get(self):
        raise NotImplementedError("The get() method has to implemented by a InputModule child class.")

    def get_id():
        raise NotImplementedError("The get_id() method has to implemented by a InputModule child class.")

    def decode(array):
        raise NotImplementedError("The decode(array) method has to implemented by a InputModule child class.")



class OutputModule(Module):
    """
    Abstract class for output modules.
    The send(binary, base64, json) and test() method have to implemented by the child class.
    """

    def __init__(self):
        super(OutputModule, self).__init__()

    def send(self, binary, base64, json):
        raise NotImplementedError("The send(binary, base64, json) method has to implemented by a OutputModule child class.")



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



class SleepModule(Module):
    """
        Abstract class for sleep() modules.
        The sleep() method has to implemented by the child class.
    """

    def __init__(self):
        super(SleepModule, self).__init__()

    def sleep(self):
        raise NotImplementedError("The sleep() method has to implemented by a SleepModule child class.")



class StatusModule(Module, LogObserver):
    """
    Abstract class for status modules.
    The status(type) method has to implemented by the child class.
    """

    def __init__(self):
        super(StatusModule, self).__init__()

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
