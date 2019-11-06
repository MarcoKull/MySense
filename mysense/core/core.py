from core.config_file import ConfigFile
from log.log import *
from modules.status_module import StatusModule

from test.test_config import test_config

import ubinascii # for base64 conversion

def __set_status(array, status):
    for s in array:
        s.set_status(status)

def __module_load(type, name):
    log_info("Loading " + type + " module '" + name + "'.")

    try:
        # this magic creates classes from knowing the type and class name only
        return getattr(__import__('modules.' + type + "." + name,[], [], [name]), name)()

    except Exception as e:
        log_error("Could not load " + type + " module '" + name + "': " + str(e) + "." )

def __modules_load(conf, type):
    modules = []
    for i in str(conf.get(type)).split(" "):
        m = __module_load(type, i)
        if m != None:
            modules.append(m)
    return modules

def run():
    log_info("MySense started.")

    # load config file
    conf = ConfigFile(
        "config/core.conf",
        (
            ("platform", "LoPy4", "Specifies the platform module. Only one module allowed", ConfigFile.VariableType.string),
            ("input", "DateTime", "Specifies the input modules using space as seperator.", ConfigFile.VariableType.string),
            ("output", "Print", "Specifies the input modules using space as seperator.", ConfigFile.VariableType.string),
            ("status", "LoPy4StatusLED Print", "Specifies the status modules using space as seperator.", ConfigFile.VariableType.string),
            ("sleep", "Software", "Specifies the sleeping module. Only one module allowed", ConfigFile.VariableType.string)
        )
    )

    # load platform module
    platform = __module_load("platform", conf.get("platform"))

    # fallback to generic platform
    if platform == None:
        log_warning("Defaulting to generic platform.")
        platform = __module_load("platform", "Generic")

        # could not load any platform module. This is fatal.
        if platform == None:
            return


    # load status modules
    status = __modules_load(conf, "status")

    # set status indicators to booting
    __set_status(status, StatusModule.StatusType.booting)

    # ota update ?
    # if otacondition: TODO
    #__set_status(status, StatusModule.StatusType.ota)

    # load input modules
    input = __modules_load(conf, "input")
    if len(input) == 0:
        log_warning("No input module loaded.")

    # load output modules
    output = __modules_load(conf, "output")
    if len(output) == 0:
        log_warning("No output module loaded.")

    # load sleep module
    sleep = __module_load("sleep", conf.get("sleep"))
    if sleep == None:
        log_warning("No sleep module loaded.")

    # run tests if platform tells so
    if platform.is_run_tests():
        # set testing mode
        __set_status(status, StatusModule.StatusType.testing)

        # general test
        test()

        # test loaded modules
        log_debug("Testing platform module '" + platform.__class__.__name__ + "'.")
        platform.test()

        log_debug("Testing sleep module '" + sleep.__class__.__name__ + "'.")
        sleep.test()

        for s in status:
            log_debug("Testing status module '" + s.__class__.__name__ + "'.")
            s.test()

        for i in input:
            log_debug("Testing input module '" + i.__class__.__name__ + "'.")
            i.test()

        for o in output:
            log_debug("Testing output module '" + o.__class__.__name__ + "'.")
            o.test()


    # keep on measuring and sending
    while True:

        # go in measuring mode
        __set_status(status, StatusModule.StatusType.measuring)

        # binary data for encoded sending
        binary = bytearray()

        # string for decoded sending
        json = ""

        for i in input:
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
            binary.append(i.get_id())

            # add data size
            binary.append(l)

            # add measurement array
            for j in m:
                binary.append(j)

            # add decoded json
            json += i.decode(m)

        # skip sending if no data
        if len(binary) == 0:
            log_info("Nothing to send.")

        else:
            # transform binary data to a base64 string
            log_debug("Decoding input with base64.")
            base64 = "".join(map(chr, ubinascii.b2a_base64(binary))).rstrip()

            # send data
            __set_status(status, StatusModule.StatusType.sending)

            for o in output:
                log_debug("Sending to output module '" + o.__class__.__name__ + "'.")
                o.send(binary, base64, json)

        # go to sleep
        __set_status(status, StatusModule.StatusType.sleeping)
        sleep.sleep()

    # this should not be reached
    __set_status(status, StatusModule.StatusType.error)
    log_error("MySense stopped.")

def test():
    log_info("Running tests.")

    log_debug("Running config file test.")
    test_config()
