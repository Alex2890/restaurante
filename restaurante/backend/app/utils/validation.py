import re

def validate_email(email):
    """Validate email format using regex"""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def validate_password(password):
    """Validate password strength
    
    Requirements:
    - At least 8 characters
    - Contains at least one digit
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    """
    if len(password) < 8:
        return False
    
    # Check for at least one digit
    if not any(char.isdigit() for char in password):
        return False
    
    # Check for at least one uppercase letter
    if not any(char.isupper() for char in password):
        return False
    
    # Check for at least one lowercase letter
    if not any(char.islower() for char in password):
        return False
    
    return True

def validate_phone(phone):
    """Validate phone number format
    
    Accepts formats like:
    - (123) 456-7890
    - 123-456-7890
    - 123.456.7890
    - 1234567890
    """
    phone_regex = r'^\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})$'
    return re.match(phone_regex, phone) is not None