"""
main.py
The main entry point for the Churn Prediction Data Engineering pipeline.
"""
import logging
from src.pipeline import run_de_pipeline
from src import config

# Setup basic logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main() -> None:
    """
    Orchestrates the pipeline execution by passing configurations to the pipeline function.
    """
    try:
        run_de_pipeline(
            input_path=config.RAW_DATA_PATH,
            output_path=config.PROCESSED_DATA_PATH,
            target=config.TARGET,
            num_cols=config.NUMERIC_COLS,
            cat_cols=config.CATEGORICAL_COLS,
            final_cols=config.COLUMNS_TO_KEEP
        )
        print("Success: Churn pipeline completed!")
        logger.info("Success: Churn pipeline completed!")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        #logging.error(f"Pipeline failed: {e}")

if __name__ == "__main__":
    main()