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

from core.modules import SleepModule
from core.config_file import ConfigFile
from core.log import *
from core.devices import I2C_Device

class DS3231(SleepModule, I2C_Device):
    """
    Adds support for wakeup by external interrupt by using the DS3231 RTCC module.
    """

    def __init__(self):
        from modules.sleep.DS3231.dep.rtc_ds3231 import RTC_DS3231
        SleepModule.__init__(self)
        I2C_Device.__init__(self, "RTC-DS3231", RTC_DS3231.I2C_ADDR, self.config().get("pin_sda"), self.config().get("pin_scl"))
        self.rtc = RTC_DS3231(self.i2c)

    def get_config_definition():
        return (
            "sleep_ds3231",
            "This module uses an external interrupt by the RTCC DS3231 to wake up.",
            (
                ("pin_sda", "20", "Defines the sda pin.", ConfigFile.VariableType.uint),
                ("pin_scl", "21", "Defines the scl pin.", ConfigFile.VariableType.uint),
                ("pin_wake", "13", "Defines the sda pin.", ConfigFile.VariableType.uint),
                ("seconds", "3", "Defines how many seconds to sleep, maximum is 59.", ConfigFile.VariableType.uint),
                ("minutes", "0", "Defines how many minutes to sleep, maximum is 59.", ConfigFile.VariableType.uint),
                ("hours", "0", "Defines how many hours to sleep, maximum is 23.", ConfigFile.VariableType.uint),
            )
        )

    def sleep(self):
        from modules.sleep.DS3231.dep.rtc_ds3231 import RTC_DS3231

        # set time to zero
        self.rtc.time_year = 1970
        self.rtc.time_month = 1
        self.rtc.time_day = 1
        self.rtc.time_workday = 1
        self.rtc.time_hours = 0
        self.rtc.time_minutes = 0
        self.rtc.time_seconds = 0

        # Set Alarm Date
        self.rtc.alarm1_day = 1
        self.rtc.alarm1_hours = self.config().get("hours")
        self.rtc.alarm1_minutes = self.config().get("minutes")
        self.rtc.alarm1_seconds = self.config().get("seconds")

        # Set Alarm Mode (see datasheet for available modes)
        self.rtc.alarm1_mode = RTC_DS3231.AlarmMode.MATCH_DATE

        # Enable Alarm
        self.rtc.alarm1_enabled = True

        # Clear Alarm Flag (this has to be called every time after a alarm occured)
        self.rtc.alarm1_clear()

        # Enable Interrupt on Alarm
        self.rtc.interrupt_enabled = True

        # Define wakup pin
        from machine import Pin
        p = Pin('P' + str(self.config().get("pin_wake")), mode=Pin.IN)

        # Define Sleep Wakeup
        import machine
        #machine.pin_deepsleep_wakeup([p], machine.WAKEUP_ALL_LOW, True)   # on older firmware
        machine.pin_sleep_wakeup([p], machine.WAKEUP_ALL_LOW, True)       # on newer firmware

        # now we can sleep finally
        machine.deepsleep()

    def test(self):
        pass
