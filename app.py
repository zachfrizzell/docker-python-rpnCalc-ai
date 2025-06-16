# app.py
import math
import re

# Custom exception for all expression-related errors
class ExpressionError(Exception):
    pass


# ============================================================================
# TOKENIZATION FUNCTIONS
# ============================================================================

def tokenize(expression: str) -> list:
    """
    Convert a mathematical expression string into a list of tokens.
    
    Args:
        expression (str): The mathematical expression to tokenize
        
    Returns:
        list: A list of tokens (numbers, operators, parentheses)
        
    Raises:
        ExpressionError: For invalid characters or malformed expressions
    """
    tokens = []
    i = 0
    
    while i < len(expression):
        char = expression[i]
        
        # Skip whitespace
        if char.isspace():
            i += 1
            continue
            
        # Handle numbers (including decimals and scientific notation)
        elif char.isdigit() or char == '.':
            number, new_i = parse_number(expression, i)
            tokens.append(number)
            i = new_i
            
        # Handle operators
        elif char in '+-*/%':
            tokens.append(char)
            i += 1
            
        # Handle parentheses
        elif char in '()':
            tokens.append(char)
            i += 1
            
        # Invalid character
        else:
            raise ExpressionError("Invalid character in expression")
    
    return tokens


def parse_number(expression: str, start_index: int) -> tuple:
    """
    Parse a number from the expression starting at the given index.
    
    Args:
        expression (str): The full expression string
        start_index (int): Starting position to parse the number
        
    Returns:
        tuple: (parsed_number, next_index)
        
    Raises:
        ExpressionError: For invalid number formats
    """
    i = start_index
    has_decimal = False
    has_e = False
    
    # Handle leading decimal point
    if expression[i] == '.':
        has_decimal = True
        i += 1
        if i >= len(expression) or not expression[i].isdigit():
            raise ExpressionError("Invalid number format")
    
    # Parse digits and special characters
    while i < len(expression):
        char = expression[i]
        
        if char.isdigit():
            i += 1
        elif char == '.' and not has_decimal and not has_e:
            has_decimal = True
            i += 1
        elif char.lower() == 'e' and not has_e and i > start_index:
            has_e = True
            i += 1
            # Handle optional sign after 'e'
            if i < len(expression) and expression[i] in '+-':
                i += 1
        else:
            break
    
    # Validate the parsed number
    number_str = expression[start_index:i]
    try:
        number = float(number_str)
        return number, i
    except ValueError:
        raise ExpressionError("Invalid number format")


# ============================================================================
# EXPRESSION VALIDATION FUNCTIONS
# ============================================================================

def validate_parentheses(tokens: list) -> None:
    """
    Check for balanced parentheses in the token list.
    
    Args:
        tokens (list): List of tokens to validate
        
    Raises:
        ExpressionError: For mismatched parentheses
    """
    open_count = 0
    
    for token in tokens:
        if token == '(':
            open_count += 1
        elif token == ')':
            open_count -= 1
            if open_count < 0:
                raise ExpressionError("Mismatched parentheses")
    
    if open_count != 0:
        raise ExpressionError("Mismatched parentheses")


def validate_unary_parentheses(tokens: list) -> None:
    """
    Validate unary expressions in parentheses and check for proper formatting.
    
    Args:
        tokens (list): List of tokens to validate
        
    Raises:
        ExpressionError: For invalid unary parentheses or number formats
    """
    i = 0
    while i < len(tokens):
        if (tokens[i] == '(' and 
            i + 1 < len(tokens) and 
            tokens[i + 1] in '+-'):
            
            # Check for unary expression: (+ or - followed by number and closing paren)
            if (i + 3 < len(tokens) and 
                isinstance(tokens[i + 2], (int, float)) and 
                tokens[i + 3] == ')'):
                
                # Validate the number format in unary context
                try:
                    float(tokens[i + 2])
                except (ValueError, TypeError):
                    raise ExpressionError("Invalid number format inside unary parenthesis")
                
                i += 4  # Skip the entire unary expression
            else:
                # Missing closing parenthesis or invalid format
                if i + 2 < len(tokens) and isinstance(tokens[i + 2], (int, float)):
                    if i + 3 >= len(tokens) or tokens[i + 3] != ')':
                        raise ExpressionError("Expected closing parenthesis after unary number")
                i += 1
        else:
            i += 1


def validate_expression_structure(tokens: list) -> None:
    """
    Validate the overall structure of the expression for proper operator/operand placement.
    
    Args:
        tokens (list): List of tokens to validate
        
    Raises:
        ExpressionError: For various structural errors
    """
    if not tokens:
        raise ExpressionError("Expression is empty")
    
    for i, token in enumerate(tokens):
        # Check for missing operators before numbers or opening parentheses
        if isinstance(token, (int, float)):
            if (i > 0 and 
                (isinstance(tokens[i-1], (int, float)) or tokens[i-1] == ')')):
                raise ExpressionError("Missing operator before number")
        
        # Check for missing operators before opening parentheses
        elif token == '(':
            if (i > 0 and 
                (isinstance(tokens[i-1], (int, float)) or tokens[i-1] == ')')):
                raise ExpressionError("Missing operator before '('")
        
        # Check for missing operands after operators
        elif token in '+-*/%':
            # Check for missing operand before closing parenthesis
            if i + 1 < len(tokens) and tokens[i + 1] == ')':
                raise ExpressionError("Missing operand before ')'")
            
            # Check for missing operand at end or before another operator
            if (i == len(tokens) - 1 or 
                (i + 1 < len(tokens) and tokens[i + 1] in '+-*/%')):
                raise ExpressionError("Missing operand")


# ============================================================================
# MATHEMATICAL OPERATION FUNCTIONS
# ============================================================================

def apply_op(operator: str, left: float, right: float) -> float:
    """
    Apply a mathematical operation to two operands.
    
    Args:
        operator (str): The operator to apply (+, -, *, /, %)
        left (float): Left operand
        right (float): Right operand
        
    Returns:
        float: Result of the operation
        
    Raises:
        ExpressionError: For division/modulo by zero or unknown operators
    """
    if operator == '+':
        return left + right
    elif operator == '-':
        return left - right
    elif operator == '*':
        return left * right
    elif operator == '/':
        if right == 0:
            raise ExpressionError("Division by zero")
        return left / right
    elif operator == '%':
        if right == 0:
            raise ExpressionError("Modulo by zero")
        return left % right
    else:
        raise ExpressionError("Unknown operator")


def get_precedence(operator: str) -> int:
    """
    Get the precedence level of an operator for proper order of operations.
    
    Args:
        operator (str): The operator to check
        
    Returns:
        int: Precedence level (higher number = higher precedence)
    """
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2}
    return precedence.get(operator, 0)


# ============================================================================
# EXPRESSION EVALUATION FUNCTIONS
# ============================================================================

def evaluate_postfix(postfix_tokens: list) -> float:
    """
    Evaluate a postfix expression using a stack-based approach.
    
    Args:
        postfix_tokens (list): List of tokens in postfix notation
        
    Returns:
        float: Result of the evaluation
        
    Raises:
        ExpressionError: For invalid expressions or mathematical errors
    """
    stack = []
    
    for token in postfix_tokens:
        if isinstance(token, (int, float)):
            stack.append(float(token))
        elif token in '+-*/%':
            if len(stack) < 2:
                raise ExpressionError("Missing operand")
            
            right = stack.pop()
            left = stack.pop()
            result = apply_op(token, left, right)
            stack.append(result)
    
    if len(stack) != 1:
        raise ExpressionError("Invalid expression")
    
    return stack[0]


def infix_to_postfix(tokens: list) -> list:
    """
    Convert infix notation to postfix notation using the Shunting Yard algorithm.
    
    Args:
        tokens (list): List of tokens in infix notation
        
    Returns:
        list: List of tokens in postfix notation
    """
    output = []
    operator_stack = []
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        # Handle numbers
        if isinstance(token, (int, float)):
            output.append(token)
        
        # Handle unary expressions in parentheses
        elif (token == '(' and 
              i + 1 < len(tokens) and 
              tokens[i + 1] in '+-' and
              i + 2 < len(tokens) and 
              isinstance(tokens[i + 2], (int, float)) and
              i + 3 < len(tokens) and 
              tokens[i + 3] == ')'):
            
            # Process unary expression: (+5) or (-3)
            sign = tokens[i + 1]
            number = tokens[i + 2]
            
            if sign == '-':
                output.append(-number)
            else:
                output.append(number)
            
            i += 3  # Skip the entire unary expression
        
        # Handle regular opening parentheses
        elif token == '(':
            operator_stack.append(token)
        
        # Handle closing parentheses
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            if operator_stack:
                operator_stack.pop()  # Remove the '('
        
        # Handle operators
        elif token in '+-*/%':
            while (operator_stack and 
                   operator_stack[-1] != '(' and
                   get_precedence(operator_stack[-1]) >= get_precedence(token)):
                output.append(operator_stack.pop())
            operator_stack.append(token)
        
        i += 1
    
    # Pop remaining operators
    while operator_stack:
        output.append(operator_stack.pop())
    
    return output


# ============================================================================
# MAIN EVALUATION FUNCTION
# ============================================================================

def evaluate(expression: str) -> float:
    """
    Main function to evaluate a mathematical expression.
    
    Args:
        expression (str): The mathematical expression to evaluate
        
    Returns:
        float: The result of the evaluation
        
    Raises:
        ExpressionError: For various parsing and evaluation errors
    """
    # Check for empty expression
    expression = expression.strip()
    if not expression:
        raise ExpressionError("Expression is empty")
    
    # Tokenize the expression
    tokens = tokenize(expression)
    
    # Validate expression structure
    validate_parentheses(tokens)
    validate_unary_parentheses(tokens)
    validate_expression_structure(tokens)
    
    # Convert to postfix and evaluate
    postfix_tokens = infix_to_postfix(tokens)
    result = evaluate_postfix(postfix_tokens)
    
    return result


# ============================================================================
# TEST CASES FOR VERIFICATION
# ============================================================================

