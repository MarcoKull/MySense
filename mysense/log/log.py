# the funcions can be used to log conviniently

from log.logger import Logger
from log.log_level import LogLevel

def log(level, message):
    Logger().log(level, message)

def log_fatal(message):
    log(LogLevel.fatal, message)

def log_error(message):
    log(LogLevel.error, message)

def log_warning(message):
    log(LogLevel.warning, message)

def log_info(message):
    log(LogLevel.info, message)

def log_debug(message):
    log(LogLevel.debug, message)
