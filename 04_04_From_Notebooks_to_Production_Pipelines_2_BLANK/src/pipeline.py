"""
src/data_pipeline.py
Orchestrates the flow of data through the extraction and transformation phases.
"""
import logging
from src.io_handler import extract_from_csv, load_to_csv
from src.preprocessing import clean_and_enrich_churn_data

#logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_de_pipeline(
    input_path: str, 
    output_path: str, 
    target: str, 
    num_cols: list[str], 
    cat_cols: list[str], 
    final_cols: list[str]
) -> None:
    """
    Runs the end-to-end Data Engineering pipeline.

    Args:
        input_path (str): Path or URL to the raw data.
        output_path (str): Path where the processed CSV will be saved.
        target (str): Name of the target column.
        num_cols (list[str]): List of numeric feature names.
        cat_cols (list[str]): List of categorical feature names.
        final_cols (list[str]): Final list of columns to export.
    """
    logger.info("Starting Data Engineering Pipeline...")
    
    # 1. Extraction
    raw_df = extract_from_csv(input_path)
    
    # 2. Transformation (Cleaning, Enrichment, and Selection)
    processed_df = clean_and_enrich_churn_data(
        df=raw_df,
        target=target,
        numeric_cols=num_cols,
        categorical_cols=cat_cols,
        final_columns=final_cols
    )
    
     # 3. Loading
    load_to_csv(processed_df, output_path)
    #processed_df.to_csv(output_path, index=False)
    logger.info(f"Pipeline finished. Processed data saved to: {output_path}")
