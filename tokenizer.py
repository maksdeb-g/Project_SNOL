# check_by_precedence() function checks the order of the operator
def get_precedence (operator):
    if operator == '+' or operator == '-':
        return 1;
    elif operator == '*' or operator == '/' or operator == '%':
        return 2;
    else:
        return -1;