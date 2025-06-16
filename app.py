import math
import re

# Custom exception for all expression-related errors
class ExpressionError(Exception):
    pass

# Tracks what kind of symbol was last seen
class SymbolType:
    NONE = 'NONE'
    NUMBER = 'NUMBER'
    OPERATOR = 'OPERATOR'
    OPEN_PAREN = 'OPEN_PAREN'
    CLOSE_PAREN = 'CLOSE_PAREN'

# Operator precedence rules
def precedence(op):
    if op in ('+', '-'): return 1
    if op in ('*', '/', '%'): return 2
    return 0

# Actually do the math
def apply_op(left, right, op):
    if op == '+': return left + right
    elif op == '-': return left - right
    elif op == '*': return left * right
    elif op == '/':
        if right == 0:
            raise ExpressionError("Division by zero")
        return left / right
    elif op == '%':
        if right == 0:
            raise ExpressionError("Modulo by zero")
        return int(left) % int(right)
    raise ExpressionError("Unknown operator")

# Main evaluator
def evaluate(expression: str) -> float:
    expression = expression.strip()
    if not expression:
        raise ExpressionError("Expression is empty")

    # Helper to check if a character is an operator
    def is_operator(c):
        return c in "+-*/%"

    # Apply top operator from the stack to the top two numbers
    def apply_top_operator():
        if len(numbers) < 2:
            raise ExpressionError("Missing operand")
        right = numbers.pop()
        left = numbers.pop()
        op = operators.pop()
        numbers.append(apply_op(left, right, op))

    numbers = []     # Number stack
    operators = []   # Operator stack
    i = 0
    last_type = SymbolType.NONE  # Keep track of last seen token type

    while i < len(expression):
        char = expression[i]

        # Ignore whitespace
        if char.isspace():
            i += 1
            continue

        # Parse a number int, float, or scientific notation
        if char.isdigit() or char == '.':
            if last_type in ('NUMBER', 'CLOSE_PAREN'):
                raise ExpressionError("Missing operator before number")

            match = re.match(r'(\d+\.\d*|\d+|\.\d+)(e[+-]?\d+)?', expression[i:])
            if not match:
                raise ExpressionError("Invalid number format")

            num_str = match.group(0)
            full_match_len = len(num_str)
            if full_match_len == 0:
                raise ExpressionError("Invalid number format")

            # Catch malformed numbers like "3.."
            next_index = i + full_match_len
            if next_index < len(expression) and expression[next_index] == '.':
                raise ExpressionError("Invalid number format")

            numbers.append(float(num_str))
            i += full_match_len
            last_type = 'NUMBER'

        # Opening parenthesis logic (also handles unary numbers like (-3))
        elif char == '(':
            if last_type in (SymbolType.NUMBER, SymbolType.CLOSE_PAREN):
                raise ExpressionError("Missing operator before '('")

            j = i + 1
            while j < len(expression) and expression[j].isspace():
                j += 1

            # Check for unary + or - inside parentheses
            if j < len(expression) and expression[j] in '+-':
                sign = -1 if expression[j] == '-' else 1
                j += 1
                while j < len(expression) and expression[j].isspace():
                    j += 1

                if j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    match = re.match(r'\d*\.?\d+(e[+-]?\d+)?', expression[j:])
                    if not match:
                        raise ExpressionError("Invalid number format inside unary parenthesis")
                    val = float(match.group(0)) * sign
                    numbers.append(val)
                    j += len(match.group(0))

                    # Skip whitespace before checking for closing paren
                    while j < len(expression) and expression[j].isspace():
                        j += 1
                    if j >= len(expression) or expression[j] != ')':
                        raise ExpressionError("Expected closing parenthesis after unary number")
                    i = j + 1
                    last_type = SymbolType.CLOSE_PAREN
                    continue

            # Regular open parenthesis
            operators.append('(')
            i += 1
            last_type = SymbolType.OPEN_PAREN

        # Handle closing parentheses
        elif char == ')':
            if last_type in (SymbolType.OPERATOR, SymbolType.OPEN_PAREN):
                raise ExpressionError("Missing operand before ')'")
            while operators and operators[-1] != '(':
                apply_top_operator()
            if not operators or operators[-1] != '(':
                raise ExpressionError("Mismatched parentheses")
            operators.pop()  # Remove the '('
            i += 1
            last_type = SymbolType.CLOSE_PAREN

        # Handle regular operators
        elif is_operator(char):
            if last_type in (SymbolType.OPERATOR, SymbolType.NONE, SymbolType.OPEN_PAREN):
                raise ExpressionError("Missing operand")
            while operators and precedence(operators[-1]) >= precedence(char):
                apply_top_operator()
            operators.append(char)
            i += 1
            last_type = SymbolType.OPERATOR

        # Invalid character found
        else:
            raise ExpressionError("Invalid character in expression")

    # Final cleanup — apply any remaining operators
    while operators:
        if operators[-1] == '(':
            raise ExpressionError("Mismatched parentheses")
        apply_top_operator()

    # There should be exactly one result left
    if len(numbers) != 1:
        raise ExpressionError("Invalid expression")

    return numbers[0]
