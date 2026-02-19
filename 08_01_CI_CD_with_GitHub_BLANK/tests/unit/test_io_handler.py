# tests/test_io_handler.py
import pytest
import os
import sys
import pandas as pd
#from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.io_handler import extract_from_csv, load_to_csv


def test_extract_returns_dataframe(tmp_path, raw_churn_df):
    """
    Scenario: Ensure the reader always returns a pandas DataFrame.
    Goal: Data integrity. Downstream functions (preprocessing) expect a DataFrame.
    """
    # Arrange
    file_path = tmp_path / "type_check.csv"
    raw_churn_df.to_csv(file_path, index=False)
    
    # Act
    df = extract_from_csv(str(file_path))
    
    # Assert
    assert isinstance(df, pd.DataFrame)

def test_extract_local_file_success(tmp_path, raw_churn_df):
    
    """
    Scenario: User provides a valid local path.
    Goal: Ensure the function reads a standard CSV correctly.
    """
    # Arrange: Create a temporary CSV file
    file_path = tmp_path / "test_raw.csv"
    raw_churn_df.to_csv(file_path, index=False)
    
    # Act
    df = extract_from_csv(str(file_path))
    
    # Assert
    ##Same number of rows as the input
    assert len(df) == 3
    ##Testing if some of the columns are present:
    assert 'customerID' in df.columns

def test_extract_from_csv_not_found():
    """
    Scenario: User provides a path that does not exist.
    Goal: Verify the custom error message and logging trigger.
    """ 
    with pytest.raises(FileNotFoundError):
        extract_from_csv("non_existent_path.csv")

def test_load_to_csv_success(tmp_path, raw_churn_df):
    """
    Scenario: Saving a processed DataFrame to a local path.
    Goal: Ensure 'to_csv' is executed and the file actually appears on disk.
    """
    # Arrange: Setup target path
    output_path = tmp_path / "results" / "output.csv"
    
    # Act: Attempt to save
    load_to_csv(raw_churn_df, str(output_path))
    
    # Assert: Check if file exists and content is correct
    assert os.path.exists(output_path)
    # Verification: Read it back to ensure it wasn't corrupted during write
    check_df = pd.read_csv(output_path)
    assert check_df.iloc[0]["customerID"] == 1


##Empty dataset
def test_extract_empty_dataset(tmp_path, empty_churn_df):
    """
    Scenario: The CSV file exists but is empty (only headers or totally empty).
    Goal: Ensure the script handles empty sources without crashing.
    """
    # Arrange: Create a CSV with only headers
    file_path = tmp_path / "empty.csv"
    empty_churn_df.to_csv(file_path, index=False)
    
    #pd.DataFrame(columns=['customerID', 'Churn']).to_csv(file_path, index=False)
    
    # Act
    df = extract_from_csv(str(file_path))
    
    # Assert
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0  # Should return 0 rows
    assert 'customerID' in df.columns # Headers should still exist