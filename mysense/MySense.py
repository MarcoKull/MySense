# this file is a shortcut for calling run and test functions

from core.core import Core

print("\nUsage:\n")
print("  MySense.run()            - Run the main application and stay in measurement loop.")
print("  MySense.test()           - Tests the main application and modules and exit.")
print("  MySense.config()         - Configure application and modules.")
print("  MySense.decode(\"str\")  - Decode a measuring string.")
print("  MySense.default_config() - Create default configuration files. Does not overwrite existing files.")
print()

def run():
    Core().run()

def test():
    print("Sorry, test() is not implemented yet.")
    pass

def config():
    print("Sorry, config() is not implemented yet.")
    pass

def decode(str):
    print("Sorry, decode(str) is not implemented yet.")
    pass

def default_config():
    Core.default_config()
