# tests/test_pipeline.py
import pytest
import os
import sys
#from unittest.mock import patch, MagicMock
import pandas as pd

# Path hack
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.pipeline import run_de_pipeline

def test_run_de_pipeline_success(tmp_path, 
                                 raw_churn_df, 
                                 pipeline_params):
    """
    Scenario: End-to-End Integration Test using real file system (tmp_path).
    Goal: Ensure the 'orchestrator' successfully moves data from input to output.
    """
    # 1. Arrange: Create a real raw file
    input_file = tmp_path / "raw_churn.csv"
    output_file = tmp_path / "processed_churn.csv"
    raw_churn_df.to_csv(input_file, index=False)
    
    # 2. Act: Run the full pipeline
    run_de_pipeline(
        input_path=str(input_file),
        output_path=str(output_file),
        target=pipeline_params["target"],
        num_cols=pipeline_params["numeric_cols"],
        cat_cols=pipeline_params["categorical_cols"],
        final_cols=pipeline_params["final_columns"]
    )
    
    # 3. Assert: Verify the output file exists and has the final expected columns
    assert os.path.exists(output_file)
    result_df = pd.read_csv(output_file)
    assert list(result_df.columns) == pipeline_params["final_columns"]
    assert len(result_df) == 3




### NOTE: This test is a bit complex, review if we add it

def test_pipeline_failure_propagation_real():
    """
    Scenario: Real-world failure propagation.
    Goal: Verify that if the file is missing, the pipeline raises FileNotFoundError.
    Method: No mocking, just passing a non-existent path.
    """
    # Arrange: A path we know is fake
    fake_path = "data/raw/this_file_does_not_exist_anywhere.csv"
    
    # Act & Assert: Using pytest.raises (Pytest's built-in tool)
    with pytest.raises(FileNotFoundError):
        run_de_pipeline(
            input_path=fake_path,
            output_path="wont_be_created.csv",
            target="Churn",
            num_cols=[],
            cat_cols=[],
            final_cols=[]
        )