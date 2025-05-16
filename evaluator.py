# === evaluator.py ===

import io_handler as io

def expression_data_type(postfix: str) -> bool:
    """
    Determine the data type of the expression based on the presence of a decimal point.
    
    Args:
        postfix (str): The postfix expression.
    
    Returns:
        bool: True if the expression is integer-only, False if it contains floats.
    """
    return '.' not in postfix  # True - integer, False - float

def evaluate_float_expression(postfix: str) -> str:
    """
    Evaluate a postfix expression containing floating-point numbers.
    
    Args:
        postfix (str): The postfix expression to evaluate.
    
    Returns:
        str: The result of the evaluation or an error message.
    """
    mystack = []  # Stack to hold operands
    tokens = postfix.split()  # Split the postfix expression into tokens

    for token in tokens:
        if token.replace('.', '', 1).isdigit() or (token[0] == '-' and token[1:].replace('.', '', 1).isdigit()):
            # Push numeric tokens onto the stack
            mystack.append(float(token))
        elif token in '+-*/':
            # Perform arithmetic operations
            if len(mystack) < 2:
                return "Error! Invalid expression."
            val2 = mystack.pop()
            val1 = mystack.pop()

            if token == '+':
                mystack.append(val1 + val2)
            elif token == '-':
                mystack.append(val1 - val2)
            elif token == '*':
                mystack.append(val1 * val2)
            elif token == '/':
                if val2 == 0:
                    return "Division by zero is not allowed!"
                mystack.append(val1 / val2)
        else:
            # Handle invalid tokens
            return "Error! Invalid token in the expression."

    if len(mystack) != 1:
        # Ensure the stack contains exactly one result
        return "Error! Invalid expression."

    result = mystack.pop()
    # Return the result as an integer if applicable, otherwise as a float
    return str(int(result)) if io.num_data_type(result) else str(result)

def evaluate_int_expression(postfix: str) -> str:
    """
    Evaluate a postfix expression containing integers.
    
    Args:
        postfix (str): The postfix expression to evaluate.
    
    Returns:
        str: The result of the evaluation or an error message.
    """
    mystack = []  # Stack to hold operands
    tokens = postfix.split()  # Split the postfix expression into tokens

    for token in tokens:
        if token.lstrip('-').isdigit():
            # Push numeric tokens onto the stack
            mystack.append(int(token))
        elif token in '+-*/%':
            # Perform arithmetic operations
            if len(mystack) < 2:
                return "Error! Invalid expression."
            val2 = mystack.pop()
            val1 = mystack.pop()

            if token == '+':
                mystack.append(val1 + val2)
            elif token == '-':
                mystack.append(val1 - val2)
            elif token == '*':
                mystack.append(val1 * val2)
            elif token == '/':
                if val2 == 0:
                    return "Division by zero is not allowed!"
                mystack.append(val1 / val2)
            elif token == '%':
                # Handle modulo operation
                if not (isinstance(val1, int) and isinstance(val2, int)):
                    return "Modulo only allowed on integers."
                if val2 == 0:
                    return "Modulo by zero is not allowed!"
                mystack.append(val1 % val2)
        else:
            # Handle invalid tokens
            return "Error! Invalid token in the expression."

    if len(mystack) != 1:
        # Ensure the stack contains exactly one result
        return "Error! Invalid expression."

    result = mystack.pop()
    # Return the result as an integer if applicable, otherwise as a float
    return str(int(result)) if io.num_data_type(result) else str(result)

def error_finder(postfix: str) -> bool:
    """
    Check if all operands in a postfix expression are of the same data type.
    
    Args:
        postfix (str): The postfix expression to check.
    
    Returns:
        bool: True if all operands are of the same type, False otherwise.
    """
    tokens = postfix.split()  # Split the postfix expression into tokens
    prev_type = None  # Track the type of the previous operand

    for token in tokens:
        is_number = token.lstrip('-').replace('.', '', 1).isdigit()
        if is_number:
            # Determine the type of the current operand (1 for integer, 0 for float)
            curr_type = 1 if '.' not in token else 0
            if prev_type is not None and curr_type != prev_type:
                # If types mismatch, return False
                return False
            prev_type = curr_type
    return True  # All operands are of the same type