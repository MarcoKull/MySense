class Module():
    """
    Abstract Module class.
    The test() method has to implemented by the child class.
    """

    def __init__(self):
        pass

    def test(self):
        raise NotImplementedError("The test() method has to implemented by a Module child class.")
