# io_handler.py

import pandas as pd
import os

def load_csv(filepath):
    """Reads a CSV file. Raises FileNotFoundError if path doesn't exist."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    return pd.read_csv(filepath)


def save_to_csv(df, filepath):
    """Saves a DataFrame to CSV, creating directories if needed."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)