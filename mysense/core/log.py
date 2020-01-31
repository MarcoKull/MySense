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

# the funcions can be used to log conviniently

#from core.logger import Logger
#from core.log_level import LogLevel

# enumeration representing the log levels
class LogLevel():
    fatal = 0
    error = 1
    warning = 2
    info = 3
    debug = 4
    all = 5

from core.logger import Logger
def log(level, message):
    Logger().log(level, message)

def log_fatal(message):
    log(LogLevel.fatal, message)

def log_error(message):
    log(LogLevel.error, message)

def log_warning(message):
    log(LogLevel.warning, message)

def log_info(message):
    log(LogLevel.info, message)

def log_debug(message):
    log(LogLevel.debug, message)

def log_all(message):
    log(LogLevel.all, message)
