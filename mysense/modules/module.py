from core.config_file import ConfigFile

class Module():
    """
    Abstract Module class.
    The test() ad get_config_definition() method has to implemented by the child class.
    """

    def __init__(self):
        # get config definitions
        cd = self.__class__.get_config_definition()

        # create config file
        self.__conf = self.__class__.create_config(cd)

    def test(self):
        raise NotImplementedError("The test() method has to implemented by a Module child class.")

    def get_config_definition():
        raise NotImplementedError("The get_config_definition() method has to implemented by a Module child class.")

    def create_config(config_definition):
        # module does not need a config file
        if config_definition == None:
            return None

        # create config file
        return ConfigFile(
            "config/" + config_definition[0] + ".conf",
            config_definition[1],
            config_definition[2]
        )

    def config(self):
        return self.__conf
