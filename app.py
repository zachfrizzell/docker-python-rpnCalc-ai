import math

# custom error to raise
class InvalidRPNString(Exception):
    pass

def calculate_rpn_method(input_string: str) -> float:
    

    MAX_CHARS = 1000
    characters = input_string.split()

   

    # stack to hold numbers during calculation
    rpn_stack = []

    # supported operators
    valid_operators = "+-*/^%"

    # go through each character (could be a number or operator)
    for char in characters:
            num = float(char)
            rpn_stack.append(num)

            if len(rpn_stack) < 2:
                raise InvalidRPNString("too few arguments")

            # pop the last two numbers from the stack
            b = rpn_stack.pop()
            a = rpn_stack.pop()

            # do the math
            if char == '+':
                result = a + b
            elif char == '-':
                result = a - b
            

    return rpn_stack.pop()

