# calculations.py
def divide(a, b):
    """Divides a by b. Raises ValueError if b is zero."""
    if b == 0:
        raise ValueError("EROOR!!")
    return a / b