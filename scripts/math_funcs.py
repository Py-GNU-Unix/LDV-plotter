#     This file is part of LDV-plotter.
# 
#     LDV-plotter is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     LDV-plotter is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with LDV-plotter.  If not, see <https://www.gnu.org/licenses/>.

# Copyright 2020-present Py-GNU-Unix <py.gnu.unix.moderator@gmail.com>

"A sandboxed commands env"

import math

pow = math.pow
abs = abs
max = max
min = min

sqrt = math.sqrt
floor = math.floor
ceil = math.ceil
log = math.log
sin = math.sin

pi = math.pi
e = math.e
inf = math.inf
nan = math.nan
tau = math.tau
cos = math.cos



del __builtins__, math, __cached__
del __doc__, __file__, __loader__
del __name__, __package__, __spec__
