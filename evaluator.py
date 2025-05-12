import io_handler as io 

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
