
import math

# custom error to raise
class InvalidRPNString(Exception):
    pass

def calculate_rpn_method(input_string: str) -> float:
    if not input_string:
        raise InvalidRPNString("empty")
    
    # Split into tokens and check length
    tokens = input_string.split()
    if len(tokens) > 1000:
        raise InvalidRPNString("input too long")
    
    # Stack to hold numbers during calculation
    rpn_stack = []
    
    # Supported operators
    valid_operators = "+-*/^%"
    
    # Go through each token
    for token in tokens:
        # Check if it's an operator
        if token in valid_operators:
            # Need at least two numbers on the stack for an operation
            if len(rpn_stack) < 2:
                raise InvalidRPNString("too few arguments")
            
            # Pop the last two numbers from the stack
            b = rpn_stack.pop()
            a = rpn_stack.pop()
            
            # Perform the operation
            if token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            elif token == '*':
                result = a * b
            elif token == '/':
                if b == 0:
                    raise InvalidRPNString("cannot divide by 0")
                result = a / b
            elif token == '^':
                try:
                    result = math.pow(a, b)
                    if math.isinf(result) or math.isnan(result):
                        raise InvalidRPNString("numerical overflow or invalid result")
                except (OverflowError, ValueError):
                    raise InvalidRPNString("invalid power operation")
            elif token == '%':
                if b == 0:
                    raise InvalidRPNString("cannot modulo by 0")
                result = a % b
            
            # Push the result back to the stack
            rpn_stack.append(result)
        else:
            # Try to convert to float
            try:
                num = float(token)
                rpn_stack.append(num)
            except ValueError:
                raise InvalidRPNString("invalid character")
    
    # After processing all tokens, we should have exactly one result
    if len(rpn_stack) == 0:
        raise InvalidRPNString("too few arguments")
    elif len(rpn_stack) > 1:
        raise InvalidRPNString("too many arguments")
    
    # Get the final result
    final_result = rpn_stack.pop()
    
    # Check for inf or nan
    if math.isinf(final_result) or math.isnan(final_result):
        raise InvalidRPNString("numerical overflow or invalid result")
    
    return final_result
