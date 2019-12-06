from core.config_file import ConfigFile
from core.log import *
from core.modules import Module, StatusModule

from core.test.tests import run_tests

import ubinascii # for base64 conversion
import uos # for listdir()
import sys # for printing exception tracebacks

class Core(Module):
    """
    This class represents the core application.
    """

    def __init__(self):

        # set status to none for exception handling
        self.__status = None

        try:
            super(Core, self).__init__()
            self.__state = StatusModule.StatusType.booting

            # set configurable variables
            self.__encoded = self.config().get("encode_measurements")
            Logger().level = self.config().get("log_level")
            Logger().use_timestamps = self.config().get("log_timestamps")

            # load platform module
            self.__platform = Module.load_module("platform", self.config().get("platform"))

            # load status modules
            self.__status = Module.load_modules(self.config(), "status")

            # set status indicators to booting
            self.__set_status(StatusModule.StatusType.booting)

            # add status modules as log observers
            for s in self.__status:
                Logger().add(s)

            # load input modules
            self.__input = Module.load_modules(self.config(), "input")
            if len(self.__input) == 0:
                log_warning("No input module loaded.")

            # load output modules
            self.__output = Module.load_modules(self.config(), "output")
            if len(self.__output) == 0:
                log_warning("No output module loaded.")

            # load sleep module
            self.__sleep = Module.load_module("sleep", self.config().get("sleep"))

        except Exception as e:
            self.__fatal(e)

    def __fatal(self, exception):
        if self.__status != None:
            self.__set_status(StatusModule.StatusType.error)

        self.__state = StatusModule.StatusType.error
        log_fatal(str(exception))
        sys.print_exception(exception)

    def __test(self):
        # set testing mode
        self.__set_status(StatusModule.StatusType.testing)

        # general tests
        self.__class__.test()

        # test loaded modules
        log_debug("Testing platform module '" + self.__platform.__class__.__name__ + "'.")
        self.__platform.test()

        log_debug("Testing sleep module '" + self.__sleep.__class__.__name__ + "'.")
        self.__sleep.test()

        for s in self.__status:
            log_debug("Testing status module '" + s.__class__.__name__ + "'.")
            s.test()

        for i in self.__input:
            log_debug("Testing input module '" + i.__class__.__name__ + "'.")
            i.test()

        for o in self.__output:
            log_debug("Testing output module '" + o.__class__.__name__ + "'.")
            o.test()

    def test():
        run_tests()

    def run(self):
        try:
            # don't run if in error mode
            if self.__state == StatusModule.StatusType.error:
                return

            # run tests if platform tells so
            if self.__platform.is_run_tests():
                self.__test()


            # keep on measuring and sending
            while True:

                # go in measuring mode
                self.__set_status(StatusModule.StatusType.measuring)

                # binary data for encoded sending
                binary = bytearray()

                # string for decoded sending
                json = ""

                for i in self.__input:
                    log_debug("Reading input module '" + i.__class__.__name__ + "'.")

                    # get measurement
                    m = i.get()
                    l = len(m)

                    # check length
                    if l == 0:
                        log_warning("Ignored input module '" + i.__class__.__name__ + "' - no data.")
                        continue

                    # add device id and length if measurement string should be encoded
                    if self.__encoded:
                        if l > 255:
                            log_error("Ignored input module '" + i.__class__.__name__ + "' - data packet too big.")
                            continue

                        # add device id
                        binary.append(i.__class__.get_id())

                        # add data size
                        binary.append(l)

                    # add measurement array
                    for j in m:
                        binary.append(j)

                    # add decoded json
                    if json != "":
                        json += ","
                    json += "\n" + i.__class__.decode(m)

                # add outer json curly braces
                json = "{" + json + "\n}"

                # skip sending if no data
                if len(binary) == 0:
                    log_warning("Nothing to send.")

                else:
                    # transform binary data to a base64 string
                    base64 = "".join(map(chr, ubinascii.b2a_base64(binary))).rstrip()
                    json_base64 = "".join(map(chr, ubinascii.b2a_base64(json))).rstrip()

                    # set outputs on status modules
                    for s in self.__status:
                        s.measurement(json)

                    # send data
                    self.__set_status(StatusModule.StatusType.sending)
                    for o in self.__output:
                        log_debug("Sending to output module '" + o.__class__.__name__ + "'.")
                        o.send(binary, base64, json, json_base64)

                # go to sleep
                self.__set_status(StatusModule.StatusType.sleeping)
                self.__sleep.sleep()

            # this should not be reached
            self.__set_status(StatusModule.StatusType.error)
            log_fatal("MySense stopped.")

        except Exception as e:
            self.__fatal(e)


    def get_config_definition():
        return (
            "core",
            "In this file you specify which modules should be used.",
            (
                ("platform", "LoPy4", "Specifies the platform module. Only one module allowed", ConfigFile.VariableType.string),
                ("input", "DateTime", "Specifies the input modules using space as seperator.", ConfigFile.VariableType.string),
                ("output", "Print", "Specifies the input modules using space as seperator.", ConfigFile.VariableType.string),
                ("status", "StatusLED Print", "Specifies the status modules using space as seperator.", ConfigFile.VariableType.string),
                ("sleep", "Soft", "Specifies the sleeping module. Only one module allowed", ConfigFile.VariableType.string),
                ("encode_measurements", "true", "Encode the measurement sting.\nIf this is set the device id and length of the data packet is added to every input module.\nThis makes it easy to convert the measurements to JSON format, but it adds an overload of 2 bytes per input module.\n\nEnable this if you have many input modules that you need to decode.", ConfigFile.VariableType.bool),
                ("log_level", "info", "Defines the minimal log level to be printed.", ConfigFile.VariableType.loglevel),
                ("log_file", "", "Path to a log file.", ConfigFile.VariableType.string),
                ("log_timestamps", "false", "Use timestamps in logs.", ConfigFile.VariableType.bool)
            )
        )

    def __set_status(self, status):
        self.state = status
        for s in self.__status:
            s.status(status)

    def default_config():
        # create core config
        Module.create_config(Core.get_config_definition())

        # iterate over module types
        for i in ("input", "output", "platform", "sleep", "status"):
            # list module folder
            for j in Module.list_modules(i):

                # load module class
                klass = Module.load_class(i, j)

                # skip unloadable classes
                if klass == None:
                    continue

                # get config definition
                cd = klass.get_config_definition()

                # skip if module has no configuration
                if cd == None:
                    continue

                # create configuration file
                Module.create_config(cd)

    def __decode(array):
        # create an array of all the input modules
        modules = [None] * 256

        for i in Module.list_modules("input"):
            klass = Module.load_class("input", i)
            if modules[klass.get_id()] != None:
                Exception("Input module id " + str(klass.get_id()) + " is used by multiple classes, run tests for more information.")
            modules[klass.get_id()] = klass

        # first check if we have a valid measurement array by adding together
        # the lengths and checking if it fits the size
        l = len(array)
        if l < 2:
            raise Exception("invalid measurement string - too small")

        s = 0
        while s < l:
            if modules[array[s]] == None:
                raise Exception("invalid measurement string - unknown input module id")

            if array[s + 1] == 0:
                raise Exception("invalid measurement string - length cannot be zero")
            s += array[s + 1]

        if l != s:
            raise Exception("invalid measurement string - lenght does not add up")

        # decoded string
        s = ""

        # read counter
        c = 0

        while c < l:
            # input module id
            id = array[c]

            # measurement length
            ml = array[c + 1]

            # measurement array
            ma = bytearray(ml)
            for i in range(0, ml):
                ma[i] = array[c + 2 + i]

            # set read counter
            c = c + 2 + ml

            # add to decoded string
            if len(s) != 0:
                s += ",\n"
            s += modules[id].decode(ma)

        return "{\n" + s + "\n}"

    def __decode_base64(str):
        return Core.__decode(ubinascii.a2b_base64(str))

    def decode(str):
        return Core.__decode_base64(str)
