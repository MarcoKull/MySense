# this file is a shortcut for calling run and test functions

from core.core import Core

#print("\nUsage:\n")
#print("  MySense.run()            - Run the main application and stay in measurement loop.")
#print("  MySense.test()           - Tests the main application and modules and exit.")
#print("  MySense.decode(\"str\")    - Decode a measuring string.")
#print("  MySense.default_config() - Create default configuration files. Does not overwrite existing files.")
#print()

def run():
    Core().run()

def test():
    Core.test()

def decode(str):
    return Core.decode(str)

def lopy4_lora_device_id():
    from network import LoRa
    import binascii
    lora = LoRa(mode=LoRa.LORAWAN)
    return binascii.hexlify(lora.mac()).upper().decode('utf-8')

def default_config():
    Core.default_config()
