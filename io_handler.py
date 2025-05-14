import re

def manual():
    """
    Displays the SNOL Help Manual and waits for user confirmation to continue.
    """
    print()
    print("=====================================================================================")
    print(" CMSC 124 Final Requirement: SNOL (Simple Number-Only Language) Help Manual")
    print("=====================================================================================")

    # 1. FORMATTING
    print("1. FORMATTING")
    print("   Tokens may be separated by spaces but it is not required.")
    print("   Commands can have no spaces. Identifiers and keywords are case-sensitive.")
    print("     Examples:")
    print("       var = 17         -> one space between tokens")
    print("       var, VaR, VAR    -> different identifiers based on case")
    print("-------------------------------------------------------------------------------------")

    # 2. DATA TYPE
    print("2. DATA TYPE")
    print("   Two data types only: integer and float. No declarations needed.")
    print("   Data type is inferred from your input values.")
    print("     Examples:")
    print("       num = 5 + 5       -> int")
    print("       num = 5.5 + 5.5   -> float")
    print("       num = 5 + 5.5     -> INVALID (mixed types)")
    print("-------------------------------------------------------------------------------------")

    # 3. ARITHMETIC OPERATIONS
    print("3. ARITHMETIC OPERATIONS")
    print("   All operands (numbers/values) must have the same data type.  ")
    print("   Infix notation is the expected format of user input.")
    print("   C-like precedence and associativity rules will be followed .")
    print("-------------------------------------------------------------------------------------")

    # 4. VARIABLES
    print("4. VARIABLES")
    print("   Variable names cannot be keywords. They may include letters and digits,")
    print("   and must be defined before use. Variables hold evaluated expressions.")
    print("-------------------------------------------------------------------------------------")

    # 5. COMMANDS
    print("5. COMMANDS")
    print("   Any valid literal, variable, or operation is a command except")
    print("   reserved keywords that trigger special behavior in the program.")
    print("-------------------------------------------------------------------------------------")

    # 6. SPECIAL KEYWORDS
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


# Determines the type of SNOL command based on the input string.
# Returns an integer code for use in a switch-like structure:
# 1 = BEG, 2 = PRINT, 3 = EXIT!, 4 = Expression, 5 = Assignment, 6 = HELP, 7 = Simple expression, 0 = Unknown
def commands(input_str: str) -> int:
    if re.fullmatch(r"BEG\s+\S+", input_str): # BEG <var> input command
        return 1
    elif re.fullmatch(r"PRINT\s+\S+", input_str): # PRINT <var> or PRINT <literal>
        return 2
    elif input_str == "EXIT!": # Exit command
        return 3
    elif input_str == "HELP": # Help command
        return 6
    elif is_variable(input_str) or is_digit(input_str): # Simple variable or literal expression (e.g., "num" or "42")
        return 7
    
    elif '=' in input_str: # Assignment (must contain '=')
        return 5
    elif any(op in input_str for op in "+-*/%"): # Arithmetic expression with operator(s) but no '='
        return 4
    return 0 # If none matched, return 0 (unknown command)


# syntax_validation() - A function to validate if the input is a valid command - Maxwell
# Accepts a string and an integer type
# Returns True if the input is valid, otherwise returns False
def syntax_validation(input_str: str, type_: int) -> bool:
    var_pattern = r"\(*-?[A-Za-z][A-Za-z0-9]*\)*"
    digit_pattern = r"\(*-?[0-9][0-9]*(\.[0-9]+)?\)*"

    parenthesis = 0
    temp = ''

    # BEG Command
    if type_ == 1:
        temp = input_str[4:].strip()
        if re.fullmatch(var_pattern, temp):
            return True
        else:
            print(f"SNOL> [{temp}] is not a valid variable name!")
            return False

    # PRINT Command
    elif type_ == 2:
        temp = input_str[6:].strip()
        if re.fullmatch(var_pattern, temp) or re.fullmatch(digit_pattern, temp):
            return True
        else:
            print("SNOL> Unknown command! Does not match any valid command of the language.")
            return False

    # Expression
    elif type_ == 4:
        for i in range(len(input_str)):
            ch = input_str[i]
            if parenthesis < 0:
                print("SNOL> Missing parenthesis pair!")
                return False
            if ch == '(':
                parenthesis += 1
                temp += ch
            elif ch == ')':
                parenthesis -= 1
                temp += ch
            elif is_operator(ch):
                if ch == '-' and i + 1 < len(input_str) and input_str[i + 1].isdigit():
                    temp += ch
                    continue
                if len(temp.strip()) == 0:
                    print("SNOL> Unknown command! Does not match any valid command of the language.")
                    return False
                if not (re.fullmatch(var_pattern, temp.strip()) or re.fullmatch(digit_pattern, temp.strip())):
                    print("SNOL> Unknown command! Does not match any valid command of the language.")
                    return False
                if ch == '/' and i + 1 < len(input_str) and input_str[i + 1] == '0':
                    print("SNOL> Division by zero is not allowed!")
                    return False
                temp = ''
            elif ch == ' ':
                continue
            else:
                temp += ch
        if parenthesis != 0:
            print("SNOL> Missing parenthesis pair!")
            return False
        if len(temp.strip()) == 0 or not (re.fullmatch(var_pattern, temp.strip()) or re.fullmatch(digit_pattern, temp.strip())):
            print("SNOL> Unknown command! Does not match any valid command of the language.")
            return False
        return True

    # Assignment Operation
    elif type_ == 5:
        equals = 0
        for i in range(len(input_str)):
            ch = input_str[i]
            if parenthesis < 0:
                print("SNOL> Missing parenthesis pair!")
                return False
            if ch == '(':
                parenthesis += 1
                temp += ch
            elif ch == ')':
                parenthesis -= 1
                temp += ch
            elif ch == '=':
                equals += 1
                if equals > 1:
                    print("SNOL> Invalid! More than one '=' in the expression.")
                    return False
                if not re.fullmatch(var_pattern, temp.strip()):
                    print("SNOL> Error! Invalid variable name syntax.")
                    return False
                temp = ''
            elif is_operator(ch):
                if ch == '-' and len(temp.strip()) == 0:
                    temp += ch
                    continue
                if len(temp.strip()) == 0 or equals == 0:
                    print("SNOL> Unknown command! Does not match any valid command of the language.")
                    return False
                if not (re.fullmatch(var_pattern, temp.strip()) or re.fullmatch(digit_pattern, temp.strip())):
                    print("SNOL> Unknown command! Does not match any valid command of the language.")
                    return False
                temp = ''
            elif ch == ' ':
                continue
            else:
                temp += ch
        if parenthesis != 0:
            print("SNOL> Missing parenthesis pair!")
            return False
        if len(temp.strip()) == 0 or not (re.fullmatch(var_pattern, temp.strip()) or re.fullmatch(digit_pattern, temp.strip())):
            print("SNOL> Unknown command! Does not match any valid command of the language.")
            return False
        return True

    # Unknown type
    else:
        return False



