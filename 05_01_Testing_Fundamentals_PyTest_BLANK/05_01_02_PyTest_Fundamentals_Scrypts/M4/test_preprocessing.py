# test_preprocessing.py
import pytest
import pandas as pd
import numpy as np
from preprocessing import (
                            convert_price_column, fill_missing_prices,
                            add_total_column, categorise_order_size
                            )

# --- Type conversion tests ---
def test_convert_price_column_numeric():
    """String prices should become floats."""
    df = pd.DataFrame({'price': ['10.50', '25.00', '7.99']})
    result = convert_price_column(df)
    assert pd.api.types.is_numeric_dtype(result['price'])
    assert result['price'][0] == 10.50



def test_add_total_column():
    """Total should be quantity * price."""
    #Arrange
    df = pd.DataFrame({'quantity': [2, 5, 1], 
                       'price': [10.0, 3.50, 100.0]})
    #Act
    # Apply function
    result_df = add_total_column(df)
 
    # Check that total column was added
    assert 'total' in result_df.columns
 
    # AssertCheck that totals are correct
    expected_totals = [10.0, 40.0, 90.0]
    assert result_df['total'].tolist() == expected_totals
    
    ##Assert
    assert 'total' in result_df.columns
    assert result_df['total'][0] == 20.0
    assert result_df['total'][1] == 17.5
    #

### Exercise 4.1: Write Your Own Tests

#Given the functions on preprocessing.py, write tests for:

#1. What happens when `add_total_column` receives a DataFrame where `quantity` is zero?
#2. What happens when `convert_price_column` receives a DataFrame where ALL prices are valid numbers? (No NaN should be created.)
#3. Does `categorise_order_size` assign `'Large'` to a quantity of exactly `11`?