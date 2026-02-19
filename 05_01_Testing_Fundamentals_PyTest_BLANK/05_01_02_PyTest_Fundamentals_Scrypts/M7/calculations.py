# calculations.py

def calculate_charge_ratio(total_charges, tenure):
    """Calculates average charges per tenure period."""
    return total_charges / (tenure + 1)

def apply_tax(price, tax_rate=0.20):
    """Applies tax to a price."""
    return price * (1 + tax_rate)

def compute_average(values):
    """Returns the mean of a list of numbers."""
    return sum(values) / len(values)