# tests/conftest.py
import pytest
import pandas as pd
import numpy as np

@pytest.fixture
def sample_orders():
    """Shared test data available to ALL test files automatically."""
    return pd.DataFrame({
        'order_id': ['ORD001', 'ORD002', 'ORD003'],
        'quantity': [2, 15, 5],
        'price': ['12.50', '45.00', ' '],
        'region': ['North', 'South', 'North']
    })

@pytest.fixture
def pipeline_config():
    """Shared configuration for pipeline tests."""
    return {
        "target": "is_premium",
        "numeric_cols": ["quantity", "price"],
        "categorical_cols": ["region"],
    }

@pytest.fixture
def clean_orders():
    """Pre-cleaned numeric data — for tests that don't need to test cleaning."""
    return pd.DataFrame({
        'order_id': ['ORD001', 'ORD002', 'ORD003'],
        'quantity': [2, 15, 5],
        'price': [12.50, 45.00, 8.00],
        'region': ['North', 'South', 'North']
    })


### Exercise 5.1: Create a Fixture

#Write a fixture called `messy_sales` that returns a DataFrame with these characteristics:

#- 4 rows
#- Columns: `product`, `quantity`, `price`
#- At least one `price` value that is a string space `' '`
#- At least one `quantity` that is `0`

#Then write one test that uses it.