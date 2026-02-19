# string_utils.py
def clean_name(name):
    """Strips whitespace and converts to title case."""
    return name.strip().title()

def is_valid_email(email):
    """Very basic email check: must contain @ and a dot after it."""
    if "@" not in email:
        return False
    parts = email.split("@")
    return "." in parts[1]

def calculate_discount(price, discount_pct):
    """Applies a percentage discount. Returns the final price."""
    return round(price * (1 - discount_pct / 100), 2)