# app.py
import math

# custom error to raise
class InvalidRPNString(Exception):
    pass

def calculate_rpn_method(input_string: str) -> float:
    # Check if input is empty
    if not input_string.strip():
        raise InvalidRPNString("empty")

    MAX_CHARS = 1000
    characters = input_string.split()
    
    # Check if input is too long
    if len(characters) > MAX_CHARS:
        raise InvalidRPNString("input too long")

    # stack to hold numbers during calculation
    rpn_stack = []

    # supported operators
    valid_operators = "+-*/^%"

    # go through each character (could be a number or operator)
    for char in characters:
        if char in valid_operators:
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
            elif char == '*':
                result = a * b
            elif char == '/':
                if b == 0:
                    raise InvalidRPNString("cannot divide by 0")
                result = a / b
            elif char == '^':
                try:
                    result = a ** b
                    if math.isinf(result) or math.isnan(result):
                        raise InvalidRPNString("numerical overflow or invalid result")
                except (OverflowError, ValueError):
                    raise InvalidRPNString("invalid power operation")
            elif char == '%':
                if b == 0:
                    raise InvalidRPNString("cannot modulo by 0")
                result = a % b
            
            rpn_stack.append(result)
        else:
            # Try to convert to number
            try:
                num = float(char)
                rpn_stack.append(num)
            except ValueError:
                raise InvalidRPNString("invalid character")

    # Check if there are too many arguments
    if len(rpn_stack) != 1:
        raise InvalidRPNString("too many arguments")
    
    # Get the final result
    result = rpn_stack.pop()
    
    # Check for inf or nan
    if math.isinf(result) or math.isnan(result):
        raise InvalidRPNString("numerical overflow or invalid result")
        
    return result
