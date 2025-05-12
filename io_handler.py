import re

def num_data_type(num: float) -> bool:
    # Checks if the float has no decimal part, i.e., it's actually an integer.
    # Example: 5.0 == 5 -> True, so it's treated as int
    #          5.3 == 5 -> False, so it's a real float
    return num == int(num)

# Checks if the string is a valid variable name based on SNOL's rules:
# Starts with a letter, followed by letters or digits.
def is_variable(s: str) -> bool:
    return re.fullmatch(r"[a-zA-Z][a-zA-Z0-9]*", s) is not None

# Checks if the string is a valid number (integer or floating-point)
# Allows negative sign and optional decimal part.
def is_digit(s: str) -> bool:
    return re.fullmatch(r"-?\d+(\.\d+)?", s) is not None