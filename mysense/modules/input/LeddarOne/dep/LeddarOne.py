#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#
from modules.input.LeddarOne.dep.serial import Serial
from modules.input.LeddarOne.dep.tcp import TCP
import machine
import time
######################### RTU SERIAL MODBUS #########################
class LeddarOne():

    def __init__(self):
        uart_id = 0x01
        self.modbus_obj = Serial(uart_id, baudrate=115200, pins=('P3', 'P4'))

    def read_input_registers(self):
        slave_addr=0x01
        starting_address=24
        register_quantity=1
        signed=False
        register_value = self.modbus_obj.read_input_registers(slave_addr, starting_address, register_quantity, signed)
        print('Input register value: ' + ' '.join('{:d}'.format(x) for x in register_value))
        print(type(register_value[0]))
        return register_value[0]