# pipeline.py
import pandas as pd
import numpy as np

def run_mini_pipeline(df, target_col):
    """
    A small cleaning pipeline that:
    1. Converts price to numeric
    2. Fills missing prices with the column mean
    3. Adds a total column (quantity * price)
    4. Maps the target column to binary (Yes=1, No=0)
    """
    df = df.copy()
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['price'] = df['price'].fillna(df['price'].mean())
    df['total'] = df['quantity'] * df['price']
    df[f'{target_col}_binary'] = df[target_col].map({'Yes': 1, 'No': 0}).astype(int)
    return df