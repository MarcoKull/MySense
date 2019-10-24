# the funcions can be used to log conviniently

from mysense.log.logger import Logger
from mysense.log.log_level import LogLevel

def log_fatal(message):
    Logger().log(LogLevel.fatal, message)

def log_error(message):
    Logger().log(LogLevel.error, message)

def log_warning(message):
    Logger().log(LogLevel.warning, message)

def log_info(message):
    Logger().log(LogLevel.info, message)

def log_debug(message):
    Logger().log(LogLevel.debug, message)
