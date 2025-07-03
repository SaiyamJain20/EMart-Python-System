import re

def is_valid_email(email: str) -> bool:
    """
    Validates an email address format.
    """
    pattern = r"[^@]+@[^@]+\.[^@]+"  # Basic email validation regex
    return re.match(pattern, email) is not None

def input_non_empty(prompt: str) -> str:
    """
    Prompts the user for a non-empty string input.
    """
    while True:
        value = input(prompt).strip() 
        if value:
            return value
        else:
            print("Input cannot be empty. Please try again.") 

def input_int(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """
    Prompts the user for an integer input within an optional range.
    """
    while True:
        try:
            value = int(input(prompt).strip())
            if min_val is not None and value < min_val:
                print(f"Value must be at least {min_val}.") 
                continue
            if max_val is not None and value > max_val:
                print(f"Value must be at most {max_val}.") 
                continue
            return value 
        except ValueError:
            print("Invalid integer. Please try again.") 


def input_float(prompt: str, min_val: float = None, max_val: float = None) -> float:
    """
    Prompts the user for a float input within an optional range.
    """
    while True:
        try:
            value = float(input(prompt).strip())
            if min_val is not None and value < min_val:
                print(f"Value must be at least {min_val}.") 
                continue
            if max_val is not None and value > max_val:
                print(f"Value must be at most {max_val}.") 
                continue
            return value
        except ValueError:
            print("Invalid number. Please try again.") 
