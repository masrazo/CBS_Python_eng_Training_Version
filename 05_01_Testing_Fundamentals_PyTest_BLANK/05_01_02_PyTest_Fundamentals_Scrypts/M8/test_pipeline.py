# test_pipeline.py

import pytest
import pandas as pd
import numpy as np
from pipeline import run_mini_pipeline

@pytest.fixture
def raw_data():
    return pd.DataFrame({
        'order_id': ['A', 'B', 'C'],
        'quantity': [3, 10, 1],
        'price': ['15.00', ' ', '8.50'],
        'is_premium': ['Yes', 'No', 'Yes']
    })

def test_pipeline_runs_without_error(raw_data):
    """Smoke test: does it run at all without crashing?"""
    result = run_mini_pipeline(raw_data, target_col='is_premium')
    assert isinstance(result, pd.DataFrame)

