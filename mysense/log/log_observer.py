class LogObserver():
    """
    Abstract class for log observers.
    The log(timestamp, level, message) method has to implemented by the child class.
    """

    def __init__(self):
        pass

    def log(self, timestamp, level, message):
        raise NotImplementedError("The log(timestamp, level, message) method has to implemented by a LogObserver child class.")
