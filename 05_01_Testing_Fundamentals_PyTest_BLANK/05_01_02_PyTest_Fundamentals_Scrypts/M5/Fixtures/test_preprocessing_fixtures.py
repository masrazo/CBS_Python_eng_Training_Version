# test_preprocessing.py
import pytest
import pandas as pd
import numpy as np
from preprocessing import convert_price_column, add_total_column

# --- Tests using fixtures ---
# Notice: the parameter name matches the fixture function name.
# Pytest sees 'sample_orders' in the signature and injects the return value.

def test_convert_price_with_fixture(sample_orders):
    result = convert_price_column(sample_orders)
    assert pd.api.types.is_numeric_dtype(result['price'])
    assert np.isnan(result['price'][2])  # The space became NaN

def test_add_total_with_fixture(clean_orders):
    result = add_total_column(clean_orders)
    assert result['total'][0] == 25.0    # 2 * 12.50
    assert result['total'][1] == 675.0   # 15 * 45.00