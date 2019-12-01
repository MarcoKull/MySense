class UARTDevice(object):
    """docstring for UARTDevice."""

    __port_counter = 1
    def port_number():
        p = UARTDevice.__port_counter
        UARTDevice.__port_counter += 1
        return p
