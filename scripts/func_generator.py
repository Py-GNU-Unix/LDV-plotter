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

import math_funcs
import math

def generate_func(string):
    def calc_y(x):
        try:
            return eval(string, {'__builtins__':math_funcs}, {"x":x})
            
        except ArithmeticError:
            return math.nan
        
    return calc_y
            
if __name__ == "__main__":
    f = generate_func(input("y = "))
    
    for num in range(100):
        print(f(num))
