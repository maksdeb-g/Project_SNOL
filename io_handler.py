import re
from tokenizer import isVariable, isDigit, is_operator

def manual():
    """
    Displays the SNOL (Simple Number-Only Language) Help Manual.
    
    This manual provides detailed information about SNOL syntax, supported data types, 
    how expressions and variables work, available commands, and reserved keywords. 
    It pauses execution until the user confirms to proceed.
    """
    print()
    print("=====================================================================================")
    print(" CMSC 124 Final Requirement: SNOL (Simple Number-Only Language) Help Manual")
    print("=====================================================================================")

    # Section 1: Formatting rules and case sensitivity.
    print("1. FORMATTING")
    print("   Tokens may be separated by spaces but it is not required.")
    print("   Commands can have no spaces. Identifiers and keywords are case-sensitive.")
    print("     Examples:")
    print("       var = 17         -> one space between tokens")
    print("       var, VaR, VAR    -> different identifiers based on case")
    print("-------------------------------------------------------------------------------------")

    # Section 2: Supported data types (only integers and floats).
    print("2. DATA TYPE")
    print("   Two data types only: integer and float. No declarations needed.")
    print("   Data type is inferred from your input values.")
    print("     Examples:")
    print("       num = 5 + 5       -> int")
    print("       num = 5.5 + 5.5   -> float")
    print("       num = 5 + 5.5     -> INVALID (mixed types)")
    print("-------------------------------------------------------------------------------------")

    # Section 3: Rules for arithmetic operations.
    print("3. ARITHMETIC OPERATIONS")
    print("   All operands (numbers/values) must have the same data type.")
    print("   Infix notation is the expected format of user input.")
    print("   C-like precedence and associativity rules will be followed.")
    print("-------------------------------------------------------------------------------------")

    # Section 4: Variable usage and restrictions.
    print("4. VARIABLES")
    print("   Variable names cannot be keywords. They may include letters and digits,")
    print("   and must be defined before use. Variables hold evaluated expressions.")
    print("-------------------------------------------------------------------------------------")

    # Section 5: Valid input expressions and reserved command behavior.
    print("5. COMMANDS")
    print("   Any valid literal, variable, or operation is a command except")
    print("   reserved keywords that trigger special behavior in the program.")
    print("-------------------------------------------------------------------------------------")

    # Section 6: Keywords with special behavior in the interpreter.
    print("6. SPECIAL KEYWORDS")
    print("   > PRINT - Display a variable or literal.")
    print("       Example:")
    print("         num = 8")
    print("         PRINT num\n")
    print("   > BEG - Prompt the user for input into a variable.")
    print("       Example:")
    print("         BEG var")
    print("         (user enters value for 'var')\n")
    print("   > HELP - Shows this SNOL Help manual.\n")
    print("   > EXIT! - Terminate the program.\n")
    print("=====================================================================================\n")

    input("Press ENTER to continue...")

def commands(input_str: str) -> int:
    """
    Classifies the input string into a command category.
    
    Args:
        input_str (str): The command entered by the user.
    
    Returns:
        int: A numeric code corresponding to the type of command:
             1 = BEG variable input
             2 = PRINT statement
             3 = EXIT! command
             4 = Arithmetic expression
             5 = Assignment (with '=')
             6 = HELP request
             7 = Simple literal or variable
             0 = Unknown/invalid command
    """
     # Handle BEG with a valid variable name
    if input_str.startswith("BEG") and len(input_str) > 3:
        # Skip the first character after "BEG" and validate the rest as a variable
        variable_candidate = input_str[4:].strip()
        if isVariable(variable_candidate):
            return 1
    elif re.fullmatch(r"BEG\s+\S+", input_str):
        return 1
    elif re.fullmatch(r"PRINT\s+\S+", input_str):
        return 2
    elif input_str == "EXIT!":
        return 3
    elif input_str == "HELP":
        return 6
    elif isVariable(input_str) or isDigit(input_str):
        return 7
    elif '=' in input_str:
        return 5
    elif any(op in input_str for op in "+-*/%") or '(' in input_str or ')' in input_str:
        return 4
    return 0

def syntax_validation(input_str: str, type_: int) -> bool:
    """
    Validates whether the provided input string conforms to the rules 
    of its corresponding SNOL command type.
    
    Args:
        input_str (str): The raw user input string.
        type_ (int): The command type (as returned by `commands()`).
    
    Returns:
        bool: True if valid syntax, otherwise False.
    """
    parenthesis = 0
    temp = ''

    # Validate BEG command syntax
    if type_ == 1:
        temp = input_str[3:].strip() if input_str.startswith("BEG") else input_str[4:].strip()
        if re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", temp):
            return True
        print(f"SNOL> [{temp}] is not a valid variable name!")
        return False

    # Validate PRINT command argument (must be variable or literal)
    elif type_ == 2:
        temp = input_str[6:].strip()
        if isVariable(temp) or isDigit(temp):
            return True
        print("SNOL> Unknown command! Does not match any valid command of the language.")
        return False

    # Validate arithmetic expression for balance and invalid cases
    elif type_ == 4:
        for i in range(len(input_str)):
            ch = input_str[i]
            if ch == '(':
                parenthesis += 1
                temp += ch
            elif ch == ')':
                parenthesis -= 1
                if parenthesis < 0:
                    print("SNOL> Missing parenthesis pair!")
                    return False
                temp += ch
            elif is_operator(ch):
                # Allow unary minus (e.g., -5 or (-3))
                if ch == '-' and (i == 0 or input_str[i-1] in "(-+*/%"):
                    temp += ch
                    continue
                if len(temp.strip()) == 0 and ch != '-':
                    print("SNOL> Unknown command! Does not match any valid command of the language.")
                    return False
                if ch == '/' and i + 1 < len(input_str) and input_str[i + 1] == '0':
                    print("SNOL> Division by zero is not allowed!")
                    return False
                temp = ''
            elif ch != ' ':
                temp += ch

        if parenthesis != 0:
            print("SNOL> Missing parenthesis pair!")
            return False
        return True

    # Validate assignment expression (variable = expression)
    elif type_ == 5:
        
        left_side = ""
        right_side = ""
        
        # Split by first equals sign
        parts = input_str.split('=', 1)
        if len(parts) != 2:
            print("SNOL> Invalid assignment expression!")
            return False

        left_side = parts[0].strip()
        right_side = parts[1].strip()

        # Left side must be a valid variable
        if not isVariable(left_side):
            print("SNOL> Error! Invalid variable name syntax.")
            return False

        # Validate that parentheses in expression are balanced
        for ch in right_side:
            if ch == '(':
                parenthesis += 1
            elif ch == ')':
                parenthesis -= 1
                if parenthesis < 0:
                    print("SNOL> Missing parenthesis pair!")
                    return False

        if parenthesis != 0:
            print("SNOL> Missing parenthesis pair!")
            return False

        return True

    # Catch-all for unsupported/unknown types
    else:
        return False

def num_data_type(num):
    """
    Determines whether the number is an integer or a float.
    
    Args:
        num (float): A numeric value to check.
    
    Returns:
        bool: True if `num` is an integer, otherwise False.
    """
    return num == int(num)
