import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def is_valid_email(email):
    if not email:
        return False
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def is_valid_phone(phone):
    if not phone:
        return False
    phone = phone.strip()
    
    # Must only contain: digits, spaces, hyphens, dots, parentheses, and leading plus
    allowed_chars = re.compile(r'^[+\d\s\-\.\(\)]+$')
    if not allowed_chars.match(phone):
        return False
    
    # Remove formatting characters to simplify checking the plus and digits
    clean_val = re.sub(r'[\s\-\.\(\)]', '', phone)
    
    # After removing formatting, a plus can only exist at the very beginning
    if '+' in clean_val[1:]:
        return False
        
    if '+' in clean_val and not clean_val.startswith('+'):
        return False

    # Extract digits to check length
    digits = re.sub(r'\D', '', clean_val)
    
    # Standard phone length globally is between 8 and 15 digits
    if not (8 <= len(digits) <= 15):
        return False
        
    return True
