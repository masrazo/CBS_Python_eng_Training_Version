##test_pipeline_integration.py
import os
import pytest
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src import config
from src.pipeline import run_de_pipeline

def test_pipeline_e2e_flow(tmp_path, raw_churn_df, pipeline_params):
     
     """
    Recommended Scenario: Tests the full flow from extraction to local save.
    Uses tmp_path (pytest fixture) to avoid polluting your project with test files.
    """
     
    # --- 1. ARRANGE ---
    # Create a temporary directory for our "mock" environment
     input_dir = tmp_path / "input"
     output_dir = tmp_path / "output"
     input_dir.mkdir()
     output_dir.mkdir()

    # Save our fixture to a temporary CSV (the "raw" data)
     input_file_path = input_dir / "raw_data.csv"
     raw_churn_df.to_csv(input_file_path, index=False)
     output_file_path = output_dir / "processed_data.csv"
    
        
    # 2. Run the actual pipeline using production config values
     try:
        # --- 2. ACT ---
        run_de_pipeline(
            input_path=str(input_file_path),
            output_path=str(output_file_path),
            target=pipeline_params['target'],
            num_cols=pipeline_params['numeric_cols'],
            cat_cols=pipeline_params['categorical_cols'],
            final_cols=pipeline_params['final_columns']
        )
     except Exception as e:
        pytest.fail(f"Pipeline failed to execute end-to-end: {e}")

    # 3. Verify physical file creation (DevOps/IO Check)
     assert os.path.exists(output_file_path), "Pipeline finished but no output file was written."

    # 4. Schema Integrity Check (Data Engineering Best Practice)
     processed_df = pd.read_csv(output_file_path)
    
    # Check that all requested columns exist
     for col in pipeline_params['final_columns']:
        assert col in processed_df.columns, f"Missing expected column: {col}"
    
    # Check that churn_binary was created and is numeric
     assert pd.api.types.is_numeric_dtype(processed_df['churn_binary']), "churn_binary should be numeric."