from log.print_logger import PrintLogger # default console logger
from log.log_level import LogLevel

 # for timestamp creation
import utime

class Logger():
    """
    This is a singleton class to log the application output.
    It also acts as suject for which observers can be added to.
    Creates a print logger by default on creation.
    """

    # implements singleton behaviour by
    # using a private class variable to use for new objects
    __instance = None
    def __new__(cls):
        if Logger.__instance is None:
            # create the singleton object
            Logger.__instance = object.__new__(cls)

            # create list of observers
            Logger.__instance.observers = [PrintLogger()]
            Logger.__instance.lvl = LogLevel.info

        return Logger.__instance

    def __init__(self):
        pass

    def add(self, observer):
        """Add a LogObserver to be notified on log messages."""
        self.observers.append(observer)

    def log(self, level, message):
        """Log given message with given level."""

        if level <= self.level:
            # create timestamp
            t = utime.localtime() # get time
            ts = ""
            for i in range(0, 6):
                if t[i] < 10: # make sure that timestamp string always has the same size
                    ts += "0"
                ts += str(t[i])

            # log message on all observers
            for o in self.observers:
                o.log(ts, level, message)

    # log level
    def get_level(self):
        return self.lvl

    def set_level(self, level):
        self.lvl = level

    level = property(get_level, set_level)
