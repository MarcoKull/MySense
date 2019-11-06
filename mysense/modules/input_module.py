class InputModule():
    """
    Abstract class for input modules.
    The get(), get_id(), test() and decode(array) method has to implemented by the child class.
    The id has to be a unique integer.
    """

    def __init__(self):
        pass

    def get(self):
        raise NotImplementedError("The get() method has to implemented by a InputModule child class.")

    def get_id(self):
        raise NotImplementedError("The get_id() method has to implemented by a InputModule child class.")

    def decode(self, array):
        raise NotImplementedError("The decode(array) method has to implemented by a InputModule child class.")
