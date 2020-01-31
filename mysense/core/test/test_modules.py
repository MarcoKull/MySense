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

from core.log import *
from core.modules import Module

def test_modules():
    # load all module classes to check for import and syntax errors
    for i in ("platform", "input", "output", "sleep", "status"):
        log_info("Test loading " + i + " module classes.")
        for j in Module.list_modules(i):
            Module.load_class(i, j)

    # check if input device id's are unique
    log_info("Testing for unique input module ids.")
    ids = []
    for i in range(0, 256):
        ids.append("")

    for i in Module.list_modules("input"):
        klass = Module.load_class("input", i)
        if len(ids[klass.get_id()]) == 0:
            ids[klass.get_id()] = i
        else:
            raise Exception("Id " + str(klass.get_id()) + " should be unique but is used by input modules '" + ids[klass.get_id()] + "' and '" + i + "'.")
