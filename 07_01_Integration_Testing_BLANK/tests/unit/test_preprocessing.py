#test_preprocessing.py

import pytest
import pandas as pd
import numpy as np
import os
import sys

# Add the project root to sys.path to allow imports from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.preprocessing import (
    handle_types, impute_values, add_features, format_target, clean_and_enrich_churn_data
)
"""
# NOTE: No need to import raw_churn_df, pytest finds it in conftest.py automatically!
"""


def test_handle_types_with_fixture(raw_churn_df):
    """
    Scenario: Convert TotalCharges from string to numeric.
    Benefit: Uses the 'TotalCharges' column defined in conftest.py.
    """
    # Act
    df = handle_types(raw_churn_df)
    
    # Assert
    assert pd.api.types.is_numeric_dtype(df['TotalCharges'])
    # The ' ' value in row 2 should have become NaN
    assert np.isnan(df['TotalCharges'][1])

def test_impute_values_with_fixture(raw_churn_df, 
                                    pipeline_params):
    """
    Scenario: Fill missing values for both Numeric and Categorical.
    Goal: Verify math and mode logic using the shared dummy data.
    """
    # First, convert types so mean() works
    df = handle_types(raw_churn_df)
    
    # Act
    df = impute_values(df, 
                       pipeline_params["numeric_cols"], 
                       pipeline_params["categorical_cols"])
    
    # Assert
    # Mean of [29.85, 50.0, np.nan] is 26.61
    assert df['MonthlyCharges'][2] > 20 
    # Mode of ['DSL', 'DSL', np.nan] is 'DSL'
    assert df['InternetService'][2] == 'DSL'

def test_add_features_with_fixture(raw_churn_df):
    """
    Scenario: Engineering 'MonthlyChargeRatio'.
    Goal: Test formula using the tenure and TotalCharges from dummy data.
    """
    df = handle_types(raw_churn_df)
    
    # Act
    df = add_features(df)
    
    # Assert: For row 0, tenure is 1, TotalCharges is 29.85. Ratio: 29.85 / (1+1) = 14.925
    assert df['MonthlyChargeRatio'][0] == pytest.approx(14.925)



def test_format_target_logic(raw_churn_df, pipeline_params):
    """
    Scenario: Mapping 'Yes' to 1 and 'No' to 0 in the target column.
    Goal: Ensure 'churn_binary' is created with correct integer mapping.
    """
    # Act
    target_col = pipeline_params["target"] # 'Churn'
    result = format_target(raw_churn_df, target_col)
    
    # Assert: Check if the new column exists
    assert 'churn_binary' in result.columns
    
    # Assert: Check the mapping values [No, Yes, No] -> [0, 1, 0]
    expected_values = [0, 1, 0]
    assert result['churn_binary'].tolist() == expected_values
    
    # Assert: Check data type is numeric/int
    assert pd.api.types.is_integer_dtype(result['churn_binary']) or pd.api.types.is_numeric_dtype(result['churn_binary'])
    

def test_full_pipeline_flow(raw_churn_df, 
                            pipeline_params):
    
    #Scenario: High-level Orchestrator test (The 'Smoke Test').
    #Goal: Ensure all steps work together to produce the final schema.
    
    # Act
    result = clean_and_enrich_churn_data(
        raw_churn_df,
        target=pipeline_params["target"],
        numeric_cols=pipeline_params["numeric_cols"],
        categorical_cols=pipeline_params["categorical_cols"],
        final_columns=pipeline_params["final_columns"]
    )
    
    # Assert: Verify the shape and columns
    assert result.shape == (3, 7)
    assert list(result.columns) == pipeline_params["final_columns"]
    assert result['churn_binary'].iloc[1] == 1 # Second customer churned
