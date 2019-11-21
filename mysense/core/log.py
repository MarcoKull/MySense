# the funcions can be used to log conviniently

#from core.logger import Logger
#from core.log_level import LogLevel

# enumeration representing the log levels
class LogLevel():
    fatal = 0
    error = 1
    warning = 2
    info = 3
    debug = 4
    all = 5

from core.logger import Logger
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

def log_all(message):
    log(LogLevel.all, message)
