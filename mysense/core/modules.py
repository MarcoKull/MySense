from core.log import *
from core.logger import LogObserver
from core.config_file import ConfigFile

try:
    import os
except:
    import uos as os

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

    def list_modules(type):
        # micropython
        try:
            modules = []

            # list module directory
            for i in os.ilistdir("modules/" + type):
                # skip directories
                if i[0] == "." or i[0] == "..":
                    continue

                modules.append(i[0])

            return modules

        # python
        except:
            return os.listdir("modules/" + type)

    def load_class(type, name):
        log_debug("Loading " + type + " module class '" + name + "'.")
        try:
            # this magic creates classes from knowing the type and class name only
            return getattr(__import__('modules.' + type + "." + name + ".module",[], [], [name]), name)

        except Exception as e:
            log_fatal("Could not load " + type + " module class '" + name + "'.")
            raise e

    def load_module(type, name):
        # loading the class
        klass = Module.load_class(type, name)
        if klass == None:
            return None

        log_info("Loading " + type + " module '" + name + "'.")
        try:
            # create a class instance
            return klass()

        except Exception as e:
            log_fatal("Could not load " + type + " module '" + name + "'.")
            raise e

    def load_modules(conf, type):
        modules = []
        for i in str(conf.get(type)).split(" "):
            if len(i) != 0:
                modules.append(Module.load_module(type, i))
        return modules

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

    def bytearray_to_uint16(array, offset):
        return array[offset + 1] + (array[offset + 0] << 8)

    def uint16_to_bytearray(uint16):
        nr = int(uint16)
        arr = bytearray(2)
        arr[0] = (nr >> 8) & 0xff
        arr[1] = nr & 0xff
        return arr

    def bytearray_to_uint32(array, offset):
        return (InputModule.bytearray_to_uint16(array, offset) << 16) + InputModule.bytearray_to_uint16(array, offset + 2)

    def uint32_to_bytearray(uint32):
        nr = int(uint32)
        arr = bytearray(4)
        arr[0] = (nr >> 24) & 0xffff
        arr[1] = (nr >> 16) & 0xffff
        arr[2] = (nr >> 8) & 0xffff
        arr[3] = nr & 0xffff
        return arr

    def concat_bytearrays(arrays):
        arr = bytearray(0)
        for i in range(0, len(arrays)):
            for j in arrays[i]:
                arr.append(j)
        return arr

class OutputModule(Module):
    """
    Abstract class for output modules.
    The send(binary, base64, json) and test() method have to implemented by the child class.
    """

    def __init__(self):
        super(OutputModule, self).__init__()

    def send(self, binary, base64, json, json_base64):
        raise NotImplementedError("The send(binary, base64, json, json_base64) method has to implemented by a OutputModule child class.")



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

    def measurement(self, bytearray, json):
        raise NotImplementedError("The measurement(bytearray, json) method has to implemented by a StatusModule child class.")

    class StatusType():
        error = "error"
        booting = "booting"
        testing = "testing"
        measuring = "measuring"
        sending = "sending"
        sleeping = "sleeping"
        ota = "ota"
