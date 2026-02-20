#test/test_main.py
import pytest
from unittest.mock import patch, MagicMock
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from main import main

# @patch acts like a "hijacker". 
# It looks inside 'main.py' and replaces the real 'config' and 
# 'run_de_pipeline' with fake "Mock" objects for the duration of this test.
@patch('main.config')           # Mock object 1: mock_config
@patch('main.run_de_pipeline')  # Mock object 2: mock_pipeline
def test_main_orchestration_success(mock_pipeline, mock_config):
    """
    PURPOSE: Verify that main() is a 'good messenger'.
    Does it correctly grab values from config.py and send them to the pipeline?
    """
    
    # --- 1. ARRANGE (The Setup) ---
    # We tell our 'mock_config' stunt double to pretend it has these specific values.
    # This keeps our test isolated from whatever is actually written in the real config.py.
    mock_config.RAW_DATA_PATH = "data/raw.csv"
    mock_config.PROCESSED_DATA_PATH = "data/output.csv"
    mock_config.TARGET = "Churn"
    mock_config.NUMERIC_COLS = ["total"]
    mock_config.CATEGORICAL_COLS = ["internet"]
    mock_config.COLUMNS_TO_KEEP = ["id", "churn_binary"]

    # --- 2. ACT (The Action) ---
    # We run the main() function. 
    # Because of the @patch decorators above, when main() tries to call 
    # 'run_de_pipeline', it will actually call our 'mock_pipeline' instead.
    main()

    # --- 3. ASSERT (The Verification) ---
    # We check if the 'mock_pipeline' was called exactly once.
    # We also check if the arguments passed to it match our mock_config values.
    # This proves the "wiring" in main.py is correct.
    mock_pipeline.assert_called_once_with(
        input_path="data/raw.csv",
        output_path="data/output.csv",
        target="Churn",
        num_cols=["total"],
        cat_cols=["internet"],
        final_cols=["id", "churn_binary"]
    )


# TEST: ERROR HANDLING

@patch('main.run_de_pipeline')
@patch('main.logger')  # We intercept the 'logger' object inside main.py
def test_main_error_handling(mock_logger, mock_pipeline):
    """
    PURPOSE: Verify the 'Safety Net'.
    If the pipeline crashes, does main() catch the error and log it?
    """
    
    # --- 1. ARRANGE (The Setup) ---
    # We tell the mock_pipeline to "explode" (raise an Exception) when called.
    # This simulates a real-world error like a missing file or network failure.
    mock_pipeline.side_effect = Exception("Connection Timeout")

    # --- 2. ACT (The Action) ---
    # We run main(). 
    # If our try/except block in main.py is working, the test won't crash.
    main()

    # --- 3. ASSERT (The Verification) ---
    # Instead of checking the output, we check the Logger.
    # Did main() call logger.error() with the specific message we expected?
    # This proves that our error handling logic is actually executing.
    mock_logger.error.assert_called_once_with("Pipeline failed: Connection Timeout")