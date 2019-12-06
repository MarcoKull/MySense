from core.log import *
from core.test.test_config import test_config
from core.test.test_modules import test_modules

def run_tests():
    log_info("Running tests.")

    log_info("Running config file test.")
    test_config()

    log_info("Running module classes test.")
    test_modules()
