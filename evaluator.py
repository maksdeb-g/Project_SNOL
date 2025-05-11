def evaluate_float_expression(postfix: str) -> str:
    """Evaluate a postfix expression with floating-point numbers."""
    mystack = []
    tokens = postfix.split()  # Split the expression into tokens

    for token in tokens:
        if token.replace('.', '', 1).isdigit() or (token[0] == '-' and token[1:].replace('.', '', 1).isdigit()):
            # If token is a number (handling negative numbers as well)
            mystack.append(float(token))
        elif token in '+-*/':
            # Pop two operands from stack
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

    # Final result
    if len(mystack) != 1:
        return "Error! Invalid expression."

    result = mystack.pop()
    if isInteger(result):
        return str(int(result))  # Return as an integer if result is effectively an integer
    return str(result)  # Return as a float


