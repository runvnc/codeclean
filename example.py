#!/usr/bin/env python3
# Example file to demonstrate code_cleaner.py

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# This is a comment that would be removed with the --remove-comments flag

def calculate(a, b):
    """Add two numbers and return the result.
    
    This docstring will be preserved even with comment removal.
    """
    print(f"Calculating sum of {a} and {b}")  # This print will be removed
    logging.debug(f"Debug: a={a}, b={b}")  # This can be removed if specified
    
    # This comment explains the calculation
    result = a + b  # Simple addition
    
    print(f"Result: {result}")  # Another print to be removed
    return result


class DebugHelper:
    """A class with various debug methods to demonstrate removal."""
    
    def __init__(self):
        # Initialize the helper
        print("DebugHelper initialized")  # Will be removed
    
    def debug_print(self, message):
        """Print a debug message."""
        # This method will be kept, but calls to it can be removed
        print(f"DEBUG: {message}")
    
    def log_info(self, info):
        """Log information at info level."""
        # This comment explains the logging
        logging.info(f"INFO: {info}")  # Can be removed if logging.info is specified


def main():
    # Main function with various function calls to demonstrate removal
    
    helper = DebugHelper()  # Initialize helper (print statement will be removed)
    
    # Calculate some values
    result1 = calculate(5, 10)
    print(f"First calculation: {result1}")  # Will be removed
    
    # Use debug helper
    helper.debug_print("Testing")  # Will be kept unless 'debug_print' is specified
    helper.log_info("Program running")  # Will be kept unless 'logging.info' is specified
    
    # Final result
    print("Program completed!")  # Will be removed


if __name__ == "__main__":
    main()
