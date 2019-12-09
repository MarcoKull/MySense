class RTC_DS3231():

    I2C_ADDR   = (0x68)
    REG_SEC    = (0x00)
    REG_MIN    = (0x01)
    REG_HOUR   = (0x02)
    REG_WEEKDAY= (0x03)
    REG_DAY    = (0x04)
    REG_MONTH  = (0x05)
    REG_YEAR   = (0x06)
    REG_A1SEC  = (0x07)
    REG_A1MIN  = (0x08)
    REG_A1HOUR = (0x09)
    REG_A1DAY  = (0x0A)
    REG_A2MIN  = (0x0B)
    REG_A2HOUR = (0x0C)
    REG_A2DAY  = (0x0D)
    REG_CTRL   = (0x0E)
    REG_STA    = (0x0F)
    REG_AGOFF  = (0x10)
    REG_TEMP   = (0x11)

    class AlarmMode:
        PER_SECOND = 0
        PER_MINUTE = 1
        MATCH_SECONDS = 2
        MATCH_MINUTES = 3
        MATCH_HOURS = 4
        MATCH_DATE = 5
        MATCH_WORKDAY = 6

    def __bcd2dec(bcd):
        return (((bcd & 0xf0) >> 4) * 10 + (bcd & 0x0f))

    def __dec2bcd(dec):
        tens, units = divmod(dec, 10)
        return (tens << 4) + units

    def __read(self, reg):
        return self.i2c.readfrom_mem(RTC_DS3231.I2C_ADDR, reg, 1)[0]

    def __write(self, reg, val):
        self.i2c.writeto_mem(RTC_DS3231.I2C_ADDR, reg, val)

    def __init__(self, i2c):
        self.i2c = i2c
        # check if chip is found
        if RTC_DS3231.I2C_ADDR not in self.i2c.scan():
            raise Exception("DS3231 not found on I2C bus at %d" % RTC_DS3231.I2C_ADDR)

    # temperature
    def get_temperature(self):
        t1 = self.__read(RTC_DS3231.REG_TEMP)
        t2 = self.__read(RTC_DS3231.REG_TEMP + 1)
        if t1>0x7F:
            return t1 - t2/256 -256
        else:
            return t1 + t2/256

    temperature = property(get_temperature)

    # aging offset
    def get_aging_offset(self):
        # TODO
        raise Exception("getting the aging offset is not implemented yet, sorry")

    def set_aging_offset(self, val):
        # TODO
        raise Exception("setting the aging offset is not implemented yet, sorry")

    aging_offset = property(get_aging_offset, set_aging_offset)

    # checks
    def __check_seconds(self, val):
        if val not in range(0, 60):
            raise Exception("value for seconds has to be between 0 and 59")

    def __check_minutes(self, val):
        if val not in range(0, 60):
            raise Exception("value for minutes has to be between 0 and 59")

    def __check_hours(self, val):
        if val not in range(0, 24):
            raise Exception("value for hours has to be between 0 and 23")

    def __check_weekday(self, val):
        if val not in range(1, 8):
            raise Exception("value for weekdays has to be between 1 and 7")

    def __check_day(self, val):
        if val not in range(1, 32):
            raise Exception("value for days has to be between 1 and 31")

    def __check_month(self, val):
        if val not in range(1, 13):
            raise Exception("value for months has to be between 1 and 12")

    def __check_year(self, val):
        if val not in range(1900, 2100):
            raise Exception("value for years has to be between 1900 and 2099")

    # time seconds
    def get_time_seconds(self):
        return RTC_DS3231.__bcd2dec(self.__read(RTC_DS3231.REG_SEC))

    def set_time_seconds(self, val):
        self.__check_seconds(val)
        self.__write(RTC_DS3231.REG_SEC, RTC_DS3231.__dec2bcd(val))

    time_seconds = property(get_time_seconds, set_time_seconds)

    # time minutes
    def get_time_minutes(self):
        return RTC_DS3231.__bcd2dec(self.__read(RTC_DS3231.REG_MIN))

    def set_time_minutes(self, val):
        self.__check_minutes(val)
        self.__write(RTC_DS3231.REG_MIN, RTC_DS3231.__dec2bcd(val))

    time_minutes = property(get_time_minutes, set_time_minutes)

    # time hours
    def get_time_hours(self):
        # using 24h only here (no am/pm)
        return RTC_DS3231.__bcd2dec(self.__read(RTC_DS3231.REG_HOUR))

    def set_time_hours(self, val):
        # using 24h only here (no am/pm)
        self.__check_hours(val)
        self.__write(RTC_DS3231.REG_HOUR, RTC_DS3231.__dec2bcd(val))

    time_hours = property(get_time_hours, set_time_hours)

    # time workdays
    def get_time_workday(self):
        return RTC_DS3231.__bcd2dec(self.__read(RTC_DS3231.REG_WEEKDAY))

    def set_time_workday(self, val):
        self.__check_weekday(val)
        self.__write(RTC_DS3231.REG_WEEKDAY, RTC_DS3231.__dec2bcd(val))

    time_workday = property(get_time_workday, set_time_workday)

    # time day
    def get_time_day(self):
        return RTC_DS3231.__bcd2dec(self.__read(RTC_DS3231.REG_DAY))

    def set_time_day(self, val):
        self.__check_day(val)
        self.__write(RTC_DS3231.REG_DAY, RTC_DS3231.__dec2bcd(val))

    time_day = property(get_time_day, set_time_day)

    # time month
    def get_time_month(self):
        return RTC_DS3231.__bcd2dec(self.__read(RTC_DS3231.REG_MONTH) & 0x1f) # mask century bit

    def __write_time_month(self, year, month):
        self.__check_month(month)
        if year >= 2000:
            self.__write(RTC_DS3231.REG_MONTH, RTC_DS3231.__dec2bcd(month) | 0b10000000) # set century bit
        else:
            self.__write(RTC_DS3231.REG_MONTH, RTC_DS3231.__dec2bcd(month))

    def set_time_month(self, val):
        self.__write_time_month(self.time_year, val)

    time_month = property(get_time_month, set_time_month)

    # time year
    def get_time_year(self):
        y = RTC_DS3231.__bcd2dec(self.__read(RTC_DS3231.REG_YEAR)) + 1900
        if self.__read(RTC_DS3231.REG_MONTH) & 0b10000000: # century bit
            y += 100
        return y

    def set_time_year(self, val):
        self.__check_year(val)

        # write month to be sure century bit is written
        m = self.time_month
        self.__write_time_month(val, m)

        # prepare year value
        while val >= 100:
            val -= 100

        # now actually write value
        self.__write(RTC_DS3231.REG_YEAR, RTC_DS3231.__dec2bcd(val))

    time_year = property(get_time_year, set_time_year)

    # time
    def time(self):
        return (
            self.time_year,
            self.time_month,
            self.time_day,
            self.time_hours,
            self.time_minutes,
            self.time_seconds,
            self.time_workday)

    # alarm1 seconds
    def get_alarm1_seconds(self):
        return RTC_DS3231.__bcd2dec(self.__read(RTC_DS3231.REG_A1SEC) & 0b01111111) # mask A1M1

    def set_alarm1_seconds(self, val):
        self.__check_seconds(val)
        m1 = self.__read(RTC_DS3231.REG_A1SEC) & 0b10000000 # preserve A1M1
        self.__write(RTC_DS3231.REG_A1SEC, RTC_DS3231.__dec2bcd(val) | m1)

    alarm1_seconds = property(get_alarm1_seconds, set_alarm1_seconds)

    # alarm1 minutes
    def get_alarm1_minutes(self):
        return RTC_DS3231.__bcd2dec(self.__read(RTC_DS3231.REG_A1MIN) & 0b01111111) # mask A1M2

    def set_alarm1_minutes(self, val):
        self.__check_minutes(val)
        m2 = self.__read(RTC_DS3231.REG_A1MIN) & 0b10000000 # preserve A1M2
        self.__write(RTC_DS3231.REG_A1MIN, RTC_DS3231.__dec2bcd(val) | m2)

    alarm1_minutes = property(get_alarm1_minutes, set_alarm1_minutes)

    # alarm1 hours
    def get_alarm1_hours(self):
        # using 24h only here (no am/pm)
        return RTC_DS3231.__bcd2dec(self.__read(RTC_DS3231.REG_A1HOUR) & 0b01111111) # mask A1M3

    def set_alarm1_hours(self, val):
        # using 24h only here (no am/pm)
        self.__check_hours(val)
        m3 = self.__read(RTC_DS3231.REG_A1HOUR) & 0b10000000 # preserve A1M3
        self.__write(RTC_DS3231.REG_A1HOUR, RTC_DS3231.__dec2bcd(val) | m3)

    alarm1_hours = property(get_alarm1_hours, set_alarm1_hours)

    # alarm1 day/date
    def get_alarm1_day(self):
        return RTC_DS3231.__bcd2dec(self.__read(RTC_DS3231.REG_A1DAY) & 0b00111111) # mask A1M4 and DY/DT

    def set_alarm1_day(self, val):
        self.__check_day(val)
        m4d = self.__read(RTC_DS3231.REG_A1DAY) & 0b11000000 # preserve A1M4 and DY/DT
        self.__write(RTC_DS3231.REG_A1DAY, RTC_DS3231.__dec2bcd(val) | m4d)

    alarm1_day = property(get_alarm1_day, set_alarm1_day)

    # alarm1 mode
    def get_alarm1_mode(self):
        m1 = self.__read(RTC_DS3231.REG_A1SEC)   & 0b10000000 != 0
        m2 = self.__read(RTC_DS3231.REG_A1MIN)   & 0b10000000 != 0
        m3 = self.__read(RTC_DS3231.REG_A1HOUR)  & 0b10000000 != 0
        m4 = self.__read(RTC_DS3231.REG_A1DAY)   & 0b10000000 != 0
        dydt = self.__read(RTC_DS3231.REG_A1DAY) & 0b01000000 != 0

        if m4:
            if m3:
                if m2:
                    if m1:
                        return RTC_DS3231.AlarmMode.PER_SECOND
                    else:
                        return RTC_DS3231.AlarmMode.MATCH_SECONDS
                else:
                    return RTC_DS3231.AlarmMode.MATCH_MINUTES
            else:
                return RTC_DS3231.AlarmMode.MATCH_HOURS
        else:
            if dydt:
                return RTC_DS3231.AlarmMode.MATCH_WORKDAY
            else:
                return RTC_DS3231.AlarmMode.MATCH_DATE

    def set_alarm1_mode(self, mode):
        # preserve values
        s = self.__read(RTC_DS3231.REG_A1SEC)  & 0b01111111
        m = self.__read(RTC_DS3231.REG_A1MIN)  & 0b01111111
        h = self.__read(RTC_DS3231.REG_A1HOUR) & 0b01111111
        d = self.__read(RTC_DS3231.REG_A1DAY)  & 0b00111111

        # set bits depending on mode
        if mode == RTC_DS3231.AlarmMode.PER_SECOND:
            s |= 0b10000000
            m |= 0b10000000
            h |= 0b10000000
            d |= 0b10000000
        elif mode == RTC_DS3231.AlarmMode.PER_MINUTE:
            raise Exception("alarm1 cannot be set to 'per minute' mode ")
        elif mode == RTC_DS3231.AlarmMode.MATCH_SECONDS:
            m |= 0b10000000
            h |= 0b10000000
            d |= 0b10000000
        elif mode == RTC_DS3231.AlarmMode.MATCH_MINUTES:
            h |= 0b10000000
            d |= 0b10000000
        elif mode == RTC_DS3231.AlarmMode.MATCH_HOURS:
            d |= 0b10000000
        elif mode == RTC_DS3231.AlarmMode.MATCH_DATE:
            pass
        elif mode == RTC_DS3231.AlarmMode.MATCH_WORKDAY:
            d |= 0b01000000
        else:
            raise Exception("invalid mode passed to alarm1")

        # write values
        self.__write(RTC_DS3231.REG_A1SEC, s)
        self.__write(RTC_DS3231.REG_A1MIN, m)
        self.__write(RTC_DS3231.REG_A1HOUR, h)
        self.__write(RTC_DS3231.REG_A1DAY, d)

    alarm1_mode = property(get_alarm1_mode, set_alarm1_mode)

    # alarm1 enabled
    def get_alarm1_enabled(self):
        return self.__read(RTC_DS3231.REG_CTRL) & 0b00000001 != 0

    def set_alarm1_enabled(self, bool):
        ctrl = self.__read(RTC_DS3231.REG_CTRL)
        if bool:
            ctrl |= 0b00000001
        else:
            ctrl &= 0b11111110
        self.__write(RTC_DS3231.REG_CTRL, ctrl)

    alarm1_enabled = property(get_alarm1_enabled, set_alarm1_enabled)

    # alarm1 flag
    def get_alarm1_flag(self):
        return self.__read(RTC_DS3231.REG_STA) & 0b00000001 != 0

    def set_alarm1_flag(self, bool):
        if bool:
            raise Exception("alarm1 flag cannot be activated manually")
        else:
            self.__write(RTC_DS3231.REG_STA, self.__read(RTC_DS3231.REG_STA) & 0b11111110)

    alarm1_flag = property(get_alarm1_flag, set_alarm1_flag)

    def alarm1_clear(self):
        self.alarm1_flag = False

    # alarm1
    def alarm1(self):
        return (
            self.alarm1_day,
            self.alarm1_hours,
            self.alarm1_minutes,
            self.alarm1_seconds)

    # alarm2 minutes
    def get_alarm2_minutes(self):
        return RTC_DS3231.__bcd2dec(self.__read(RTC_DS3231.REG_A2MIN) & 0b01111111) # mask A2M2

    def set_alarm2_minutes(self, val):
        self.__check_minutes(val)
        m2 = self.__read(RTC_DS3231.REG_A2MIN) & 0b10000000 # preserve A2M2
        self.__write(RTC_DS3231.REG_A2MIN, RTC_DS3231.__dec2bcd(val) | m2)

    alarm2_minutes = property(get_alarm2_minutes, set_alarm2_minutes)

    # alarm2 hours
    def get_alarm2_hours(self):
        # using 24h only here (no am/pm)
        return RTC_DS3231.__bcd2dec(self.__read(RTC_DS3231.REG_A2HOUR) & 0b01111111) # mask A2M3

    def set_alarm2_hours(self, val):
        # using 24h only here (no am/pm)
        self.__check_hours(val)
        m3 = self.__read(RTC_DS3231.REG_A2HOUR) & 0b10000000 # preserve A2M3
        self.__write(RTC_DS3231.REG_A2HOUR, RTC_DS3231.__dec2bcd(val) | m3)

    alarm2_hours = property(get_alarm2_hours, set_alarm2_hours)

    # alarm2 day/date
    def get_alarm2_day(self):
        return RTC_DS3231.__bcd2dec(self.__read(RTC_DS3231.REG_A2DAY) & 0b00111111) # mask A2M4 and DY/DT

    def set_alarm2_day(self, val):
        self.__check_day(val)
        m4d = self.__read(RTC_DS3231.REG_A2DAY) & 0b11000000 # preserve A2M4 and DY/DT
        self.__write(RTC_DS3231.REG_A2DAY, RTC_DS3231.__dec2bcd(val) | m4d)

    alarm2_day = property(get_alarm2_day, set_alarm2_day)

    # alarm2 mode
    def get_alarm2_mode(self):
        m2 = self.__read(RTC_DS3231.REG_A2MIN)   & 0b10000000 != 0
        m3 = self.__read(RTC_DS3231.REG_A2HOUR)  & 0b10000000 != 0
        m4 = self.__read(RTC_DS3231.REG_A2DAY)   & 0b10000000 != 0
        dydt = self.__read(RTC_DS3231.REG_A2DAY) & 0b01000000 != 0

        if m4:
            if m3:
                if m2:
                    return RTC_DS3231.AlarmMode.PER_MINUTE
                else:
                    return RTC_DS3231.AlarmMode.MATCH_MINUTES
            else:
                return RTC_DS3231.AlarmMode.MATCH_HOURS
        else:
            if dydt:
                return RTC_DS3231.AlarmMode.MATCH_WORKDAY
            else:
                return RTC_DS3231.AlarmMode.MATCH_DATE

    def set_alarm2_mode(self, mode):
        # preserve values
        m = self.__read(RTC_DS3231.REG_A2MIN)  & 0b01111111
        h = self.__read(RTC_DS3231.REG_A2HOUR) & 0b01111111
        d = self.__read(RTC_DS3231.REG_A2DAY)  & 0b00111111

        # set bits depending on mode
        if mode == RTC_DS3231.AlarmMode.PER_SECOND:
            raise Exception("alarm2 cannot be set to 'per second' mode ")
        elif mode == RTC_DS3231.AlarmMode.PER_MINUTE:
            m |= 0b10000000
            h |= 0b10000000
            d |= 0b10000000
        elif mode == RTC_DS3231.AlarmMode.MATCH_SECONDS:
            raise Exception("alarm2 cannot be set to 'match seconds' mode ")
        elif mode == RTC_DS3231.AlarmMode.MATCH_MINUTES:
            h |= 0b10000000
            d |= 0b10000000
        elif mode == RTC_DS3231.AlarmMode.MATCH_HOURS:
            d |= 0b10000000
        elif mode == RTC_DS3231.AlarmMode.MATCH_DATE:
            pass
        elif mode == RTC_DS3231.AlarmMode.MATCH_WORKDAY:
            d |= 0b01000000
        else:
            raise Exception("invalid mode passed to alarm2")

        # write values
        self.__write(RTC_DS3231.REG_A2MIN, m)
        self.__write(RTC_DS3231.REG_A2HOUR, h)
        self.__write(RTC_DS3231.REG_A2DAY, d)

    alarm2_mode = property(get_alarm2_mode, set_alarm2_mode)

    # alarm2 enabled
    def get_alarm2_enabled(self):
        return self.__read(RTC_DS3231.REG_CTRL) & 0b00000010 != 0

    def set_alarm2_enabled(self, bool):
        ctrl = self.__read(RTC_DS3231.REG_CTRL)
        if bool:
            ctrl |= 0b00000010
        else:
            ctrl &= 0b11111101
        self.__write(RTC_DS3231.REG_CTRL, ctrl)

    alarm2_enabled = property(get_alarm2_enabled, set_alarm2_enabled)

    # alarm2 flag
    def get_alarm2_flag(self):
        return self.__read(RTC_DS3231.REG_STA) & 0b00000010 != 0

    def set_alarm2_flag(self, bool):
        if bool:
            raise Exception("alarm2 flag cannot be activated manually")
        else:
            self.__write(RTC_DS3231.REG_STA, self.__read(RTC_DS3231.REG_STA) & 0b11111101)

    alarm2_flag = property(get_alarm2_flag, set_alarm2_flag)

    def alarm2_clear(self):
        self.alarm2_flag = False

    # alarm2
    def alarm2(self):
        return (
            self.alarm2_day,
            self.alarm2_hours,
            self.alarm2_minutes)

    # battery-backed square wave
    def get_bbsqw(self):
        return self.__read(RTC_DS3231.REG_CTRL) & 0b01000000 != 0

    def set_bbsqw(self, bool):
        ctrl = self.__read(RTC_DS3231.REG_CTRL)
        if bool:
            ctrl |= 0b01000000
        else:
            ctrl &= 0b10111111
        self.__write(RTC_DS3231.REG_CTRL, ctrl)

    bbsqw = property(get_bbsqw, set_bbsqw)

    # interrupt control
    def get_interrupt_enabled(self):
        return self.__read(RTC_DS3231.REG_CTRL) & 0b00000100 != 0

    def set_interrupt_enabled(self, bool):
        ctrl = self.__read(RTC_DS3231.REG_CTRL)
        if bool:
            ctrl |= 0b00000100
        else:
            ctrl &= 0b11111011
        self.__write(RTC_DS3231.REG_CTRL, ctrl)

    interrupt_enabled = property(get_interrupt_enabled, set_interrupt_enabled)

