# preprocessing.py
import pandas as pd
import numpy as np

def convert_price_column(df):
    """Converts a 'price' column from string to numeric. Non-numeric values become NaN."""
    df = df.copy()
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    return df

def fill_missing_prices(df, fill_value=0.0):
    """Fills NaN values in the 'price' column with a default."""
    df = df.copy()
    df['price'] = df['price'].fillna(fill_value)
    return df

def add_total_column(df):
    """Adds a 'total' column = quantity * price."""
    df = df.copy()
    df['total'] = df['quantity'] * df['price']
    return df

def categorise_order_size(df):
    """
    Adds an 'order_size' column:
    - 'Small' if quantity <= 3
    - 'Medium' if quantity <= 10
    - 'Large' if quantity > 10
    """
    df = df.copy()
    conditions = [df['quantity'] <= 3, df['quantity'] <= 10, df['quantity'] > 10]
    choices = ['Small', 'Medium', 'Large']
    df['order_size'] = np.select(conditions, choices, default='Unknown')
    return df