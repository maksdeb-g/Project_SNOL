import re
from tokenizer import isVariable, isDigit, is_operator

def manual():
    """
    Displays the SNOL Help Manual and waits for user confirmation to continue.
    Provides detailed information about the SNOL language, including formatting, data types, 
    arithmetic operations, variables, commands, and special keywords.
    """
    print()
    print("=====================================================================================")
    print(" CMSC 124 Final Requirement: SNOL (Simple Number-Only Language) Help Manual")
    print("=====================================================================================")

    # Section 1: Formatting
    print("1. FORMATTING")
    print("   Tokens may be separated by spaces but it is not required.")
    print("   Commands can have no spaces. Identifiers and keywords are case-sensitive.")
    print("     Examples:")
    print("       var = 17         -> one space between tokens")
    print("       var, VaR, VAR    -> different identifiers based on case")
    print("-------------------------------------------------------------------------------------")

    # Section 2: Data Types
    print("2. DATA TYPE")
    print("   Two data types only: integer and float. No declarations needed.")
    print("   Data type is inferred from your input values.")
    print("     Examples:")
    print("       num = 5 + 5       -> int")
    print("       num = 5.5 + 5.5   -> float")
    print("       num = 5 + 5.5     -> INVALID (mixed types)")
    print("-------------------------------------------------------------------------------------")

    # Section 3: Arithmetic Operations
    print("3. ARITHMETIC OPERATIONS")
    print("   All operands (numbers/values) must have the same data type.")
    print("   Infix notation is the expected format of user input.")
    print("   C-like precedence and associativity rules will be followed.")
    print("-------------------------------------------------------------------------------------")

    # Section 4: Variables
    print("4. VARIABLES")
    print("   Variable names cannot be keywords. They may include letters and digits,")
    print("   and must be defined before use. Variables hold evaluated expressions.")
    print("-------------------------------------------------------------------------------------")

    # Section 5: Commands
    print("5. COMMANDS")
    print("   Any valid literal, variable, or operation is a command except")
    print("   reserved keywords that trigger special behavior in the program.")
    print("-------------------------------------------------------------------------------------")

    # Section 6: Special Keywords
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
    Determines the type of SNOL command based on the input string.
    
    Args:
        input_str (str): The input command string.
    
    Returns:
        int: A code representing the command type:
             1 = BEG, 2 = PRINT, 3 = EXIT!, 4 = Expression, 
             5 = Assignment, 6 = HELP, 7 = Simple expression, 0 = Unknown.
    """
    # Fix for BEGvar command - check if input starts with BEG followed by a variable name
    if input_str.startswith("BEG") and len(input_str) > 3 and isVariable(input_str[3:]):
        return 1
    elif re.fullmatch(r"BEG\s+\S+", input_str):  # Original BEG <var> input command
        return 1
    elif re.fullmatch(r"PRINT\s+\S+", input_str):  # PRINT <var> or PRINT <literal>
        return 2
    elif input_str == "EXIT!":  # Exit command
        return 3
    elif input_str == "HELP":  # Help command
        return 6
    elif isVariable(input_str) or isDigit(input_str):  # Simple variable or literal expression
        return 7
    elif '=' in input_str:  # Assignment (must contain '=')
        return 5
    elif any(op in input_str for op in "+-*/%") or '(' in input_str or ')' in input_str:  # Arithmetic expression with operators or parentheses
        return 4
    return 0  # If none matched, return 0 (unknown command)

def syntax_validation(input_str: str, type_: int) -> bool:
    """
    Validates if the input string is a valid command based on its type.
    
    Args:
        input_str (str): The input command string.
        type_ (int): The type of command to validate (1 = BEG, 2 = PRINT, etc.).
    
    Returns:
        bool: True if the input is valid, False otherwise.
    """
    parenthesis = 0
    temp = ''

    # BEG Command Validation
    if type_ == 1:
        # Fix for BEGvar command
        if input_str.startswith("BEG") and len(input_str) > 3:
            temp = input_str[3:].strip()
        else:
            temp = input_str[4:].strip()
            
        if re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", temp):  # Variable name validation
            return True
        else:
            print(f"SNOL> [{temp}] is not a valid variable name!")
            return False

    # PRINT Command Validation
    elif type_ == 2:
        temp = input_str[6:].strip()
        if isVariable(temp) or isDigit(temp):  # Validate variable or literal
            return True
        else:
            print("SNOL> Unknown command! Does not match any valid command of the language.")
            
            return False

    # Expression Validation
    elif type_ == 4:
        # Improved expression validation to handle complex expressions like (1+3)*5
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
                # Handle negative numbers
                if ch == '-' and (i == 0 or (i > 0 and (input_str[i-1] == '(' or is_operator(input_str[i-1])))):
                    temp += ch
                    continue
                
                # Skip operator validation for complex expressions
                if len(temp.strip()) == 0 and ch != '-':
                    print("SNOL> Unknown command! Does not match any valid command of the language.")
                    return False
                
                if ch == '/' and i + 1 < len(input_str) and input_str[i + 1] == '0':
                    print("SNOL> Division by zero is not allowed!")
                    return False
                
                # Reset temp after processing an operator
                if len(temp.strip()) > 0:
                    temp = ''
            elif ch == ' ':
                continue
            else:
                temp += ch
                
        if parenthesis != 0:
            print("SNOL> Missing parenthesis pair!")
            return False
            
        # Allow empty temp at the end for complex expressions
        return True

    # Assignment Operation Validation
    elif type_ == 5:
        equals = 0
        left_side = ""
        right_side = ""
        
        # Split by first equals sign
        parts = input_str.split('=', 1)
        if len(parts) != 2:
            print("SNOL> Invalid assignment expression!")
            return False
            
        left_side = parts[0].strip()
        right_side = parts[1].strip()
        
        # Validate left side is a variable
        if not isVariable(left_side):
            print("SNOL> Error! Invalid variable name syntax.")
            return False
            
        # Validate right side has balanced parentheses
        parenthesis = 0
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
            
        # For complex expressions like (1+3)*5, we'll let the evaluator handle it
        return True

    # Unknown Command Type
    else:
        return False

def num_data_type(num):
    """
    Check if a number is an integer or float.
    
    Args:
        num (float): The number to check.
    
    Returns:
        bool: True if the number is an integer, False if it is a float.
    """
    return num == int(num)