# === symbol_table.py ===

class SymbolTable:
    def __init__(self):
        """Initialize the symbol table with an empty dictionary to store variables."""
        self.variables = {}
    
    def set_variable(self, name, value):
        """
        Set a variable in the symbol table.
        
        Args:
            name (str): The name of the variable.
            value (int/float): The value to assign to the variable.
        
        Returns:
            value: The value that was set.
        """
        self.variables[name] = value
        return value
    
    def get_variable(self, name):
        """
        Get the value of a variable from the symbol table.
        
        Args:
            name (str): The name of the variable.
        
        Returns:
            int/float/None: The value of the variable if it exists, otherwise None.
        """
        if name in self.variables:
            return self.variables[name]
        return None
    
    def variable_exists(self, name):
        """
        Check if a variable exists in the symbol table.
        
        Args:
            name (str): The name of the variable.
        
        Returns:
            bool: True if the variable exists, False otherwise.
        """
        return name in self.variables
    
    def print_all(self):
        """
        Print all variables and their values in the symbol table.
        
        This is useful for debugging or displaying the current state of the symbol table.
        """
        for name, value in self.variables.items():
            print(f"{name} = {value}")