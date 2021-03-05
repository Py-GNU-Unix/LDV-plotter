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
