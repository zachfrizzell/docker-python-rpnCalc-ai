import math

# custom error to raise
class InvalidRPNString(Exception):
    pass

def calculate_rpn_method(input_string: str) -> float:
    # trim whitespace and check if input is empty
    if input_string.strip() == "":
        raise InvalidRPNString("empty")

    # limit input size to avoid excessive processing
    MAX_CHARS = 1000
    characters = input_string.split()

    if len(characters) > MAX_CHARS:
        raise InvalidRPNString("input too long")

    # stack to hold numbers during calculation
    rpn_stack = []

    # supported operators
    valid_operators = "+-*/^%"

    # go through each character (could be a number or operator)
    for char in characters:
        try:
            # try converting character to a number
            num = float(char)
            rpn_stack.append(num)
        except ValueError:
            # check if it's a valid operator
            if char not in valid_operators:
                raise InvalidRPNString("invalid character")

            # need at least 2 numbers to do an operation
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
                   result = math.pow(a, b)
               except ValueError:
                   raise InvalidRPNString("invalid power operation")
               if math.isinf(result) or math.isnan(result):
                   raise InvalidRPNString("numerical overflow or invalid result")

            elif char == '%':
                if b == 0:
                    raise InvalidRPNString("cannot modulo by 0")
                result = a % b

            # make sure result isn’t infinite or nan
            if math.isinf(result) or math.isnan(result):
                raise InvalidRPNString("numerical overflow or invalid result")

            # push the result back on the stack
            rpn_stack.append(result)

    # make sure there is only one result
    if len(rpn_stack) != 1:
        raise InvalidRPNString("too many arguments")

    return rpn_stack.pop()
