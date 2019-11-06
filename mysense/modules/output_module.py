from modules.module import Module

class OutputModule(Module):
    """
    Abstract class for output modules.
    The send(binary, base64, json) and test() method have to implemented by the child class.
    """

    def __init__(self):
        pass

    def send(self, binary, base64, json):
        raise NotImplementedError("The send(binary, base64, json) method has to implemented by a OutputModule child class.")
