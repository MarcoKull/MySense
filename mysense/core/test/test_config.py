from core.log import *

import uos

from core.config_file import ConfigFile

PATH_TESTCONFIG="core/test/test.conf"

def file_exists(path):
    try:
        open(path, "r")
        return True
    except:
        return False

def test_config_step(conf, desc):

    # values that are not defined should return None
    if conf.get("undefined") != None:
        log_error("ConfigFile " + desc + " test failed - undefined variable was accepted.")

    # invalid variables should not show up
    if conf.get("invalidBool") != None:
        log_error("ConfigFile " + desc + " test failed - invalid boolean was accepted.")

    if conf.get("invalidUint") != None:
        log_error("ConfigFile " + desc + " test failed - invalid uint was accepted.")

    # check if stored values are correctly
    if conf.get("bool") != True:
        log_error("ConfigFile " + desc + " test failed - bool was not returned correctly.")

    if conf.get("uint") != 42:
        log_error("ConfigFile " + desc + " test failed - uint was not returned correctly.")

    if conf.get("string") != "hello world":
        log_error("ConfigFile " + desc + " test failed - string was not returned correctly.")

def test_config():
    # save log level
    level = Logger().level

    # set log level to error temporarily to mute intentional warnings
    Logger().level = LogLevel.error

    # definition of test config values
    conf_values = (
        ("bool", "true", "this is an example boolean\nsecond line", ConfigFile.VariableType.bool),
        ("uint", "42", "this is an example number", ConfigFile.VariableType.uint),
        ("string", "hello world", "this is an example string", ConfigFile.VariableType.string),

        ("invalidBool", "thisIsNoBoolean", "this is an invalid example boolean\nsecond line", ConfigFile.VariableType.bool),
        ("invalidUint", "fourtyTwo", "this is an invalid example number", ConfigFile.VariableType.uint),
    )

    if file_exists(PATH_TESTCONFIG):
        # remove test config file in case it exists
        try:
            uos.remove(PATH_TESTCONFIG)
        except:
            # some micropython distributions don't implement uos.remove()
            pass

    conf_create = ConfigFile(PATH_TESTCONFIG, "This file is just for testing.", conf_values)

    # config file should have been created now
    if not file_exists(PATH_TESTCONFIG):
        log_error("ConfigFile test failed - file was not created.")

    # run tests for newly created config file
    test_config_step(conf_create, "create")

    # create loaded config file
    conf_load = ConfigFile(PATH_TESTCONFIG, "This file is just for testing.", conf_values)

    # run tests for loaded config
    test_config_step(conf_load, "load")

    # restore log level
    Logger().level = level
