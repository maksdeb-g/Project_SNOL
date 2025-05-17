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
File: symbol_table.py

Description:
This file contains the implementation of the symbol table module for the SNOL (Simple Number Only Language) interpreter. 
The symbol table is responsible for storing and managing variables and their associated values during the execution 
of SNOL programs. It provides utility functions to set, retrieve, and check the existence of variables, as well as 
to display all stored variables for debugging purposes.
"""

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