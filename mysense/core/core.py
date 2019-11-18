from core.config_file import ConfigFile
from log.log import *
from modules.module import Module
from modules.status_module import StatusModule

from test.test_config import test_config

import ubinascii # for base64 conversion
import uos # for listdir()

class Core(Module):
    """
    This class represents the core application.
    """

    def __init__(self):
        super(Core, self).__init__()

        # set desired logging level
        Logger().level = self.config().get("loglevel")

        # load status modules
        self.__status = Core.__load_modules(self.config(), "status")

        # set status indicators to booting
        self.__set_status(StatusModule.StatusType.booting)

        # add status modules as log observers
        for s in self.__status:
            Logger().add(s)

        # load platform module
        self.__platform = Core.__load_module("platform", self.config().get("platform"))

        # fallback to generic platform
        if self.__platform == None:
            log_warning("Defaulting to generic platform.")
            self.__platform = Core.__load_module("platform", "Generic")

            # could not load any platform module. This is fatal.
            if self.__platform == None:
                return

        # load input modules
        self.__input = Core.__load_modules(self.config(), "input")
        if len(self.__input) == 0:
            log_warning("No input module loaded.")

        # load output modules
        self.__output = Core.__load_modules(self.config(), "output")
        if len(self.__output) == 0:
            log_warning("No output module loaded.")

        # load sleep module
        self.__sleep = Core.__load_module("sleep", self.config().get("sleep"))

        # fallback to generic platform
        if self.__sleep == None:
            log_warning("Defaulting to software sleep.")
            self.__sleep = Core.__load_module("sleep", "Software")

            # could not load any platform module. This is fatal.
            if self.__sleep == None:
                return

        if self.__sleep == None:
            log_warning("No sleep module loaded.")

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
        log_info("Running tests.")

        log_debug("Running config file test.")
        test_config()

    def run(self):
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
                    log_info("Ignored input module '" + i.__class__.__name__ + "' - no data.")
                    continue
                elif l > 255:
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
                log_info("Nothing to send.")

            else:
                # transform binary data to a base64 string
                log_debug("Decoding input with base64.")
                base64 = "".join(map(chr, ubinascii.b2a_base64(binary))).rstrip()

                # set outputs on status modules
                for s in self.__status:
                    s.measurement(json)

                # send data
                self.__set_status(StatusModule.StatusType.sending)
                for o in self.__output:
                    log_debug("Sending to output module '" + o.__class__.__name__ + "'.")
                    o.send(binary, base64, json)

            # go to sleep
            self.__set_status(StatusModule.StatusType.sleeping)
            self.__sleep.sleep()

        # this should not be reached
        __set_status(status, StatusModule.StatusType.error)
        log_error("MySense stopped.")

    def get_config_definition():
        return (
            "core",
            "In this file you specify which modules should be used.",
            (
                ("platform", "LoPy4", "Specifies the platform module. Only one module allowed", ConfigFile.VariableType.string),
                ("input", "DateTime", "Specifies the input modules using space as seperator.", ConfigFile.VariableType.string),
                ("output", "Print", "Specifies the input modules using space as seperator.", ConfigFile.VariableType.string),
                ("status", "StatusLED Print", "Specifies the status modules using space as seperator.", ConfigFile.VariableType.string),
                ("sleep", "Software", "Specifies the sleeping module. Only one module allowed", ConfigFile.VariableType.string),
                ("loglevel", "info", "Defines the minimal log level to be printed.", ConfigFile.VariableType.loglevel)
            )
        )

    def __set_status(self, status):
        for s in self.__status:
            s.status(status)

    def __list_modules(type):
        modules = []

        # list module directory
        for i in uos.ilistdir("modules/" + type):

            # skip directories
            if i[1] != 8:
                continue

            modules.append(i[0][:-3])

        return modules

    def default_config():
        # create core config
        Module.create_config(Core.get_config_definition())

        # iterate over module types
        for i in ("input", "output", "platform", "sleep", "status"):

            # list module folder
            for j in uos.ilistdir("modules/" + i):

                # only regard normal files
                if j[1] != 8:
                    continue

                # load module class
                klass = Core.__load_class(i, j[0][:-3])

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

    def __load_class(type, name):
        log_debug("Loading " + type + " module class '" + name + "'.")
        try:
            # this magic creates classes from knowing the type and class name only
            return getattr(__import__('modules.' + type + "." + name,[], [], [name]), name)

        except Exception as e:
            log_error("Could not load " + type + " module class '" + name + "': " + str(e) + "." )

    def __load_module(type, name):
        # loading the class
        klass = Core.__load_class(type, name)
        if klass == None:
            return None

        log_info("Loading " + type + " module '" + name + "'.")
        try:
            # create a class instance
            return klass()

        except Exception as e:
            log_error("Could not load " + type + " module '" + name + "': " + str(e) + "." )

    def __load_modules(conf, type):
        modules = []
        for i in str(conf.get(type)).split(" "):
            m = Core.__load_module(type, i)
            if m != None:
                modules.append(m)
        return modules
