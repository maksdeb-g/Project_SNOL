import re

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




