from modules.module import Module

class InputModule(Module):
    """
    Abstract class for input modules.
    The get(), get_id(), test() and decode(array) method has to implemented by the child class.
    The id has to be a unique integer.
    """

    def __init__(self):
        super(InputModule, self).__init__()

    def get(self):
        raise NotImplementedError("The get() method has to implemented by a InputModule child class.")

    def get_id():
        raise NotImplementedError("The get_id() method has to implemented by a InputModule child class.")

    def decode(array):
        raise NotImplementedError("The decode(array) method has to implemented by a InputModule child class.")
