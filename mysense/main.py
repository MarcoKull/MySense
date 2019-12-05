import MySense
import machine
if machine.reset_cause() != machine.PWRON_RESET:
    MySense.run()
