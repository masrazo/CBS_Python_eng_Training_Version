import pytest
import pandas as pd
import numpy as np
import os
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src import config

@pytest.fixture
def raw_churn_df():
    """Matches your actual CSV schema with specific edge cases."""
    return pd.DataFrame({
        'customerID': [1, 2, 3],
        'tenure': [1, 0, 24],
        'TotalCharges': ['29.85', ' ', '1889.5'], # Test: space handling
        'MonthlyCharges': [29.85, 50.0, np.nan],  # Test: numeric imputation
        'InternetService': ['DSL', 'DSL', np.nan], # Test: categorical imputation
        'Churn': ['No', 'Yes', 'No']              # Test: target mapping
    })

@pytest.fixture
def pipeline_params():
    """Provides the config variables as a dictionary for easy function passing."""
    return {
        "target": config.TARGET,
        "numeric_cols": config.NUMERIC_COLS,
        "categorical_cols": config.CATEGORICAL_COLS,
        "final_columns": ['customerID', 'tenure', 'TotalCharges', 'MonthlyCharges', 
                         'InternetService','MonthlyChargeRatio', 'churn_binary']
        #"final_columns": config.COLUMNS_TO_KEEP
    }

@pytest.fixture
def empty_churn_df():
    """Matches your actual CSV schema with specific edge cases."""
    return pd.DataFrame(columns=['customerID', 'Churn'])
