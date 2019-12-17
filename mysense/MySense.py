# this file is a shortcut for calling run and test functions

from core.core import Core

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
