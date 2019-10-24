from mysense.log.log_observer import LogObserver

class PrintLogger(LogObserver):
    """Prints log messages with timestamps."""

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

        print("[" + timestamp + "] " + l + " " + message)
