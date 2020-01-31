# This file is part of the MySense software (https://github.com/MarcoKull/MySense).
# Copyright (c) 2020 Marco Kull
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

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
