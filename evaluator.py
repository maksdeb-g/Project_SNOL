import io_handler as io 

'''
    Checks data type of an expression
    Returns True if integer, False if floating-point number
'''
def expression_data_type(postfix: str) -> bool:
    return '.' not in postfix  # True - integer, False - float


def evaluate_float_expression(postfix: str) -> str:
    """Evaluate a postfix expression with floating-point numbers."""
    mystack = []
    tokens = postfix.split()  # Split the expression into tokens

    for token in tokens:
        # Check if token is a number (including negative floats)
        if token.replace('.', '', 1).isdigit() or (token[0] == '-' and token[1:].replace('.', '', 1).isdigit()):
            mystack.append(float(token))
        elif token in '+-*/':
            # Pop two operands from stack
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
                    return "INPUT ERROR: Division by zero."
                mystack.append(val1 / val2)
        else:
            return "Error! Invalid token in the expression."

    if len(mystack) != 1:
        return "Error! Invalid expression."

    result = mystack.pop()
    return str(int(result)) if num_data_type(result) else str(result)


def evaluate_int_expression(postfix: str) -> str:
    """Evaluate a postfix expression with integers and integer-only modulo."""
    mystack = []
    tokens = postfix.split()  # Tokenize the input string by spaces

    for token in tokens:
        # Check if token is a valid integer (including negative)
        if token.lstrip('-').isdigit():
            mystack.append(int(token))  # Store as int
        elif token in '+-*/%':
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
                    return "INPUT ERROR: Division by zero."
                mystack.append(val1 / val2)
            elif token == '%':
                if not (io.num_data_type(val1) and io.num_data_type(val2)):
                    return "INPUT ERROR: Modulo only allowed on integers."
                if val2 == 0:
                    return "INPUT ERROR: Modulo by zero."
                mystack.append(val1 % val2)
        else:
            return "Error! Invalid token in the expression."

    if len(mystack) != 1:
        return "Error! Invalid expression."

    result = mystack.pop()
    return str(int(result)) if io.num_data_type(result) else str(result)


'''
    Checks errors in the postfix expression (if numbers are of the same type)
    Returns True if no errors, False if error is found
    
    Note: The argument passed to this function is the postfix expression returned from conversion_helper()
          so split() is sufficient to tokenize the expression.
'''
def error_finder(postfix: str) -> bool:
    tokens = postfix.split()     # Tokenize the postfix expression
    prev_type = None             # Track the type of the previous number

    for token in tokens:
        # Check if token is a number 
        is_number = token.lstrip('-').replace('.', '', 1).isdigit()
        
        if is_number:
            # Check type: 1 - integer, 0 - float
            curr_type = 1 if '.' not in token else 0

            if prev_type is not None and curr_type != prev_type:
                return False      # Error: mismatched types
            prev_type = curr_type

    return True                  # All numbers are of the same type
