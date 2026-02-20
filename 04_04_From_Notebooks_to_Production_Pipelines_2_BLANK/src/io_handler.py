"""
src/io_handler.py
Handles all Input/Output operations (Reading and Writing data).
"""
import pandas as pd
import logging
import os

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==========================================
# SECTION: IO_HANDLER (The source for io_handler.py)
# ==========================================
def extract_from_csv(filepath: str) -> pd.DataFrame:
    """
    Extracts data from a CSV file located locally or via a public URL.

    Args:
        filepath (str): The local path or public URL to the raw CSV file.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the raw dataset.
    """
    logger.info(f"Initiating extraction from: {filepath}")
    
    if not filepath.startswith(('http://', 'https://')):
        if not os.path.exists(filepath):
            logger.error(f"File not found: {filepath}")
            raise FileNotFoundError(f"Could not find local file at {filepath}")
    try:
        df = pd.read_csv(filepath)
        logger.info(f"Extraction successful. Loaded {len(df)} rows.")
        return df
    except Exception as e:
        logger.error(f"Failed to load data from {filepath}: {e}")
        raise RuntimeError(f"Data extraction failed: {e}")


def load_to_csv(df: pd.DataFrame, filepath: str) -> None:
    """
    Saves a DataFrame to a local CSV file. Automatically creates directories if missing.

    Args:
        df (pd.DataFrame): The processed DataFrame to save.
        filepath (str): The local path where the file should be saved.
    """
    try:
        # Create the folder if it doesn't exist (e.g., data/processed/)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        df.to_csv(filepath, index=False)
        logger.info(f"Successfully loaded data to: {filepath}")
    except Exception as e:
        logger.error(f"Failed to save data to {filepath}: {e}")
        raise RuntimeError(f"Data loading failed: {e}")