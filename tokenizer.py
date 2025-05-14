import evaluator as evaluator

# check_by_precedence() function checks the order of the operator
def get_precedence (operator):
    if operator == '+' or operator == '-':
        return 1;
    elif operator == '*' or operator == '/' or operator == '%':
        return 2;
    else:
        return -1;import re

''' Converts infix to postfix
    Prerequisite function: precedence()
    Returns the postfix expression as a string
'''

# Checks if a specific character on the string is a valid operator - Jann Dave
# Valid operators are +, -, *, /, and % (Addition, Subtraction, Multiplication, Division, and Modulo)
def is_Operator(character):
    match (character):	    
        case '+': return true
        case '-': return true
        case '*': return true
        case '/': return true
        case '%': return true
        case _: return false

# Checks if the string is a valid variable name based on SNOL's rules: - Roslyn
# Starts with a letter, followed by letters or digits.
def is_variable(s: str) -> bool:
    return re.fullmatch(r"[a-zA-Z][a-zA-Z0-9]*", s) is not None

# Checks if the string is a valid number (integer or floating-point) - Roslyn
# Allows negative sign and optional decimal part.
def is_digit(s: str) -> bool:
    return re.fullmatch(r"-?\d+(\.\d+)?", s) is not None

def conversion_helper(infix: str) -> str:

    mystack = []       # Stack for storing operators and parentheses - Janelle
    postfix = []       # List for the resulting postfix expression
    tokens = []        # List for the tokens extracted from the infix expression
    number = ""        # Temporary string to hold numbers before appending to tokens
    i = 0              # Index to track position in string

    # Tokenizer
    while i < len(infix):
        char = infix[i]

        # Ignore whitespaces and continue to next character
        if char.isspace():
            # If there's a number being built, store it as a complete token 
            if number:
                tokens.append(number)
                number = ""
            i += 1
            continue

        # Handle negative numbers
        if char == '-' and (i == 0 or infix[i - 1] in '+-*/('):    
            number += char
            i += 1
            continue

        # If it's a digit or a decimal point, keep building the number
        if char.isdigit() or char == '.':
            number += char
            i += 1
            continue

        # Add completed number to tokens 
        if number:
            tokens.append(number)
            number = ""     # Reset number string

        # If it's an operator or parenthesis, append it to tokens
        if char in '+-*/()':
            tokens.append(char)

        i += 1

    # Append any remaining number to tokens
    if number:
        tokens.append(number)


    # Process tokens to convert to postfix
    for token in tokens:
        # Check if token is a valid number
        is_valid_number = token.lstrip('-').replace('.', '', 1).isdigit()

        # If valid, append it to postfix
        if is_valid_number:
            postfix.append(token) 

        # If token is an opening parenthesis, push it to the stack
        elif token == '(':
            mystack.append(token) 

        # If token is a closing parenthesis, pop from stack and append to postfix until matching '('
        elif token == ')': 
            while mystack and mystack[-1] != '(':
                postfix.append(mystack.pop())   
            if mystack and mystack[-1] == '(':
                mystack.pop()  

        # If token is an operator
        elif token in '+-*/':
            # Pop from stack and append to postfix while top has higher or equal precedence
            while mystack and mystack[-1] != '(' and precedence(token) <= precedence(mystack[-1]):
                postfix.append(mystack.pop())   
            mystack.append(token)  # Push current operator to stack

        # Ignore invalid tokens
        else:
            continue  

    # Pop remaining operators from stack and append to postfix
    while mystack:
        postfix.append(mystack.pop())  

    return ' '.join(postfix)  # Join list into postfix string


# Converts an Infix Expression into a Postfix Expression - Jann Dave
# Uses 'evaluator.py' for helper functions
def postfix_conversion(expr):
    # Convert infix to postfix
    postfix = conversion_helper(expr)

    # Check for data type consistency
    if not evaluator.error_finder(postfix):
        print("SNOL> Error! Operands must be of the same data type in an arithmetic operation!")
        return

    else: 
        # Determine expression data type and evaluate the postfix expression
        if evaluator.expression_data_type(postfix):  # For integer data type in postfix expression
            result = evaluator.evaluate_int_exp(postfix)

            # Error Handling for non-integer types in Modulo Operation
            if result == "ERROR":
                print("SNOL> Error! Operands must be int type to perform Modulo!")
                return

        else:  # For float data type in postfix expression
            result = evaluator.evaluate_float_exp(postfix)

            # Error Handling for non-integer types in Modulo Operation
            if result == "ERROR":
                print("SNOL> Error! Operands must be int type to perform Modulo!")
                return

        # Terminate function operations
        return