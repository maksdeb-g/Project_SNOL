from tokenizer import BEG, PRINT, assignmentOp, varValidation, getValue, postfix_conversion
from io_handler import manual, syntax_validation, commands
from symbol_table import SymbolTable  # Used by tokenizer module

def main():
    """
    Entry point for the SNOL interpreter.
    Handles user input, determines the command type, and executes the appropriate functionality.
    """
    print("The SNOL environment is now active, you may proceed with giving your commands.")
    
    while True:
        # Prompt the user for input
        input_str = input("Command: ")
        
        # Determine the type of command
        command_type = commands(input_str)
        
        if command_type == 0:
            # Invalid command
            print("SNOL> Unknown command! Does not match any valid command of the language.")
            
        elif command_type == 1:  # BEG command
            # Handle variable initialization
            if syntax_validation(input_str, 1):
                BEG(input_str)
        elif command_type == 2:  # PRINT command
            # Handle printing of variables or literals
            if syntax_validation(input_str, 2):
                PRINT(input_str)
        elif command_type == 3:  # EXIT! command
            # Exit the interpreter
            print("Interpreter is now terminated...")
            break
        elif command_type == 4:  # Expression
            # Handle arithmetic expressions
            if not syntax_validation(input_str, 4):
                continue
            if varValidation(input_str):
                value = getValue(input_str)
                postfix_conversion(value)
                # Don't print anything here
        elif command_type == 5:  # Assignment
            # Handle variable assignment
            if syntax_validation(input_str, 5):
                assignmentOp(input_str)
        elif command_type == 6:  # HELP command
            # Display the help manual
            manual()
        elif command_type == 7:  # Simple expression (variable or literal)
            # Handle simple expressions (e.g., variable or literal evaluation)
            if varValidation(input_str):
                # Don't print anything here
                pass

if __name__ == "__main__":
    # Run the main function when the script is executed
    main()