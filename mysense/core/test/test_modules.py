from core.log import *
from core.modules import Module

def test_modules():
    # load all module classes to check for import and syntax errors
    for i in ("platform", "input", "output", "sleep"):
        log_info("Test loading " + i + " module classes.")
        for j in Module.list_modules(i):
            Module.load_class(i, j)

    # check if input device id's are unique
    log_info("Testing for unique input module ids.")
    ids = []
    for i in range(0, 256):
        ids.append("")

    for i in Module.list_modules("input"):
        klass = Module.load_class("input", i)
        if len(ids[klass.get_id()]) == 0:
            ids[klass.get_id()] = i
        else:
            raise Exception("Id " + str(klass.get_id()) + " should be unique but is used by input modules '" + ids[klass.get_id()] + "' and '" + i + "'.")
