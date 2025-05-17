"""
CMSC 124 Final Requirement: SNOL Interpreter
Project Description: This project implements an interpreter for the SNOL (Simple Number Only Language), 
a custom programming language designed for educational purposes. The interpreter supports basic commands 
such as variable initialization, arithmetic operations, printing, and more.

Programmers: 
- Casquejo, Jann Dave Rhodore G.
- Gazo, Maxwell Dave P.
- Guillermo, Roslyn Faith U.
- Ojanola, Janelle B.
- Organiza, Trixie Nicole A.

Date of Completion: May 17, 2025
"""

"""
File: tokenizer.py

Description:
This file contains the implementation of the tokenizer module for the SNOL (Simple Number Only Language) interpreter. 
The tokenizer is responsible for breaking down input strings into tokens, validating syntax, and converting infix 
expressions to postfix notation for evaluation. It also provides utility functions for handling variables, operators, 
and keywords in the SNOL language.
"""

import re
from symbol_table import SymbolTable

# Global symbol table instance
symbol_table = SymbolTable()

# Define keywords for the SNOL language
KEYWORDS = ["BEG", "PRINT", "EXIT!", "HELP"]

def get_precedence(operator):
    """
    Get the precedence of an operator.
    
    Args:
        operator (str): The operator to check.
    
    Returns:
        int: The precedence level (higher value = higher precedence).
    """
    if operator == '+' or operator == '-':
        return 1
    elif operator == '*' or operator == '/' or operator == '%':
        return 2
    else:
        return -1

def is_operator(character):
    """
    Check if a character is a valid operator.
    
    Args:
        character (str): The character to check.
    
    Returns:
        bool: True if the character is an operator, False otherwise.
    """
    return character in '+-*/%'

def isVariable(s: str) -> bool:
    """
    Check if a string is a valid variable name and not a keyword.
    
    Args:
        s (str): The string to check.
    
    Returns:
        bool: True if the string is a valid variable name, False otherwise.
    """
    return re.fullmatch(r"[a-zA-Z][a-zA-Z0-9]*", s) is not None and s not in KEYWORDS

def isDigit(s: str) -> bool:
    """
    Check if a string represents a valid integer or float.
    
    Args:
        s (str): The string to check.
    
    Returns:
        bool: True if the string is a valid number, False otherwise.
    """
    return re.fullmatch(r"-?\d+(\.\d+)?", s) is not None

def isKeyword(s: str) -> bool:
    """
    Check if a string is a keyword in the SNOL language.
    
    Args:
        s (str): The string to check.
    
    Returns:
        bool: True if the string is a keyword, False otherwise.
    """
    return s in KEYWORDS

def conversion_helper(infix: str) -> str:
    """
    Convert an infix expression to postfix notation.
    
    Args:
        infix (str): The infix expression to convert.
    
    Returns:
        str: The postfix expression or an error message.
    """
    mystack = []  # Stack to hold operators
    postfix = []  # List to hold the postfix expression
    tokens = []   # List to hold tokens from the infix expression
    number = ""   # Temporary variable to build multi-character tokens
    i = 0

    while i < len(infix):
        char = infix[i]

        if char.isspace():
            # Handle spaces between tokens
            if number:
                tokens.append(number)
                number = ""
            i += 1
            continue

        if char == '-' and (i == 0 or infix[i - 1] in '+-*/('):
            # Handle negative numbers
            number += char
            i += 1
            continue

        if char.isdigit() or char == '.':
            # Handle numeric tokens
            number += char
            i += 1
            continue

        if char.isalpha():
            # Handle variable names or keywords
            while i < len(infix) and (infix[i].isalnum() or infix[i] == '!'):
                number += infix[i]
                i += 1
            continue

        if number:
            # Add the completed token to the list
            tokens.append(number)
            number = ""

        if char in '+-*/()%':
            # Add operators and parentheses to the token list
            tokens.append(char)

        i += 1

    if number:
        # Add the last token if any
        tokens.append(number)

    # Check for keywords in the expression
    for token in tokens:
        if isKeyword(token):
            return "KEYWORD_ERROR"

    for token in tokens:
        is_valid_number = token.lstrip('-').replace('.', '', 1).isdigit()

        if is_valid_number:
            # Add numbers directly to the postfix expression
            postfix.append(token)
        elif isVariable(token):
            # Replace variables with their values
            if symbol_table.variable_exists(token):
                postfix.append(str(symbol_table.get_variable(token)))
            else:
                print(f"SNOL> Error! [{token}] is not defined!")
                return "ERROR"
        elif token == '(':
            mystack.append(token)
        elif token == ')':
            # Pop operators until the matching '(' is found
            while mystack and mystack[-1] != '(':
                postfix.append(mystack.pop())
            if mystack and mystack[-1] == '(':
                mystack.pop()
        elif token in '+-*/%':
            # Handle operator precedence
            while mystack and mystack[-1] != '(' and get_precedence(token) <= get_precedence(mystack[-1]):
                postfix.append(mystack.pop())
            mystack.append(token)
        else:
            continue

    while mystack:
        # Pop remaining operators
        postfix.append(mystack.pop())

    return ' '.join(postfix)

def postfix_conversion(expr):
    """
    Convert an infix expression to postfix and evaluate it.
    
    Args:
        expr (str): The infix expression to convert.
    
    Returns:
        str/None: The result of the evaluation or None if an error occurs.
    """
    from evaluator import error_finder, expression_data_type, evaluate_int_expression, evaluate_float_expression
    
    postfix = conversion_helper(expr)
    
    if postfix == "ERROR":
        return None
    elif postfix == "KEYWORD_ERROR":
        print("SNOL> Unknown command! Does not match any valid command of the language.")
        return None

    if not error_finder(postfix):
        print("SNOL> Error! Operands must be of the same type in an arithmetic operation!")
        return None
    else:
        if expression_data_type(postfix):
            result = evaluate_int_expression(postfix)
            if "Error" in result or "INPUT ERROR" in result:
                print(f"SNOL> {result}")
                return None
        else:
            result = evaluate_float_expression(postfix)
            if "Error" in result or "INPUT ERROR" in result:
                print(f"SNOL> {result}")
                return None

        # Don't print the result
        return result

def BEG(input_str):
    """
    Handle the BEG command to initialize a variable with user input.
    
    Args:
        input_str (str): The input string containing the BEG command.
        
    """
    if input_str.startswith("BEG") and len(input_str) > 3 and not input_str[3].isspace():
        var_name = input_str[3:].strip()
    else:
        var_name = input_str[4:].strip()
        
    if not isVariable(var_name):
        print(f"SNOL> [{var_name}] is not a valid variable name!")
        return
    
    print(f"SNOL> Please enter value for [{var_name}]")
    value = input("Input: ")
    
    # Determine if the input is an integer or float
    if isDigit(value):
        if '.' in value:
            symbol_table.set_variable(var_name, float(value))
        else:
            symbol_table.set_variable(var_name, int(value))
    else:
        print("SNOL> Error! Input must be a number.")

def PRINT(input_str):
    """
    Handle the PRINT command to display a variable or literal.
    
    Args:
        input_str (str): The input string containing the PRINT command.
    """
    value_to_print = input_str[6:].strip()
    
    if isDigit(value_to_print):
        print(f"SNOL> {value_to_print}")
    elif isVariable(value_to_print):
        if symbol_table.variable_exists(value_to_print):
            print(f"SNOL> [{value_to_print}] = {symbol_table.get_variable(value_to_print)}")
        else:
            print(f"SNOL> Error! [{value_to_print}] is not defined!")
    else:
        print("SNOL> Error! Invalid expression to print.")

def assignmentOp(input_str):
    """
    Handle assignment operations to assign values to variables.
    
    Args:
        input_str (str): The input string containing the assignment operation.
    """
    parts = input_str.split('=', 1)
    var_name = parts[0].strip()
    expression = parts[1].strip()
    
    if not isVariable(var_name):
        print(f"SNOL> Error! '{var_name}' is not a valid variable name.")
        return
    
    # Check if the expression contains keywords
    if any(keyword in expression for keyword in KEYWORDS):
        print("SNOL> Unknown command! Does not match any valid command of the language.")
        return
    
    # Evaluate the expression
    result = postfix_conversion(expression)
    
    if result is not None:
        # Convert result to the appropriate type
        if '.' in result:
            value = float(result)
        else:
            value = int(result)
        
        # Store in symbol table
        symbol_table.set_variable(var_name, value)

def varValidation(input_str):
    """
    Validate if all variables in an expression exist in the symbol table.
    
    Args:
        input_str (str): The input string containing the expression.
    
    Returns:
        bool: True if all variables exist, False otherwise.
    """
    # Check if the expression contains keywords
    if any(keyword in input_str for keyword in KEYWORDS):
        print("SNOL> Unknown command! Does not match any valid command of the language.")
        return False
    
    tokens = re.findall(r'[a-zA-Z][a-zA-Z0-9]*', input_str)
    
    for token in tokens:
        if isVariable(token) and not symbol_table.variable_exists(token):
            print(f"SNOL> Error! [{token}] is not defined!")
            return False
    
    return True

def getValue(input_str):
    """
    Return the input string as is for evaluation.
    
    Args:
        input_str (str): The input string.
    
    Returns:
        str: The input string.
    """
    return input_str