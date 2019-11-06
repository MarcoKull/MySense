from log.log_observer import LogObserver

class PrintLogger(LogObserver):
    """
    Prints log messages with timestamps.
    """
    def __init__(self):
        self.print_timestamp = False

    def log(self, timestamp, level, message):
        if level == 0:
            l = "Fatal:  "
        elif level == 1:
            l = "Error:  "
        elif level == 2:
            l = "Warning:"
        elif level == 3:
            l = "Info:   "
        elif level == 4:
            l = "Debug:  "
        else:
            l = "UNKNOWN!"

        msg = l + " " + message

        if self.print_timestamp:
            msg = "[" + timestamp + "] " + msg

        print(msg)
