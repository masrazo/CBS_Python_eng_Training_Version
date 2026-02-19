##Churn_preprocessing_pipeline
import pandas as pd
import logging
import os
from pathlib import Path


# Setup logging exactly like your scripts
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==========================================
# SECTION: CONFIG (The source for config.py)
# ==========================================
TARGET: str = 'Churn'

NUMERIC_COLS: list[str] = ['tenure', 'MonthlyCharges', 'TotalCharges']

CATEGORICAL_COLS: list[str] = [
    'gender', 'SeniorCitizen', 'Partner', 'Dependents', 
    'PhoneService', 'MultipleLines', 'InternetService'
]

# The final schema for the "Gold" table (Analytics/Modeling ready)
COLUMNS_TO_KEEP: list[str] = NUMERIC_COLS + CATEGORICAL_COLS + ['MonthlyChargeRatio', 'churn_binary']
#Root path:
#when move to src then 
#project_root = Path(__file__).resolve().parent.parent
##When on project use this path
project_root = Path(__file__).resolve().parent
# File Paths
##Data sources
RAW_DATA_PATH = "https://rockborne-bucket-01-cbs.s3.eu-west-2.amazonaws.com/DataSources/WA_Fn-UseC_-Telco-Customer-Churn.csv"
##Pre-process data path
CLEAN_DATA_PATH: str = "data/processed/churn_preprocessed.csv"
PROCESSED_DATA_PATH = project_root / CLEAN_DATA_PATH

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
    
    
# ==========================================
# SECTION: PREPROCESSING (The source for preprocessing.py)
# ==========================================
def handle_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts specific columns to the correct data types for analysis.

    Args:
        df (pd.DataFrame): The DataFrame to process.

    Returns:
        pd.DataFrame: DataFrame with corrected column types.
    """
    if 'TotalCharges' in df.columns:
        logger.info("Converting 'TotalCharges' to numeric.")
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    return df

def impute_values(df: pd.DataFrame, 
                  num_cols: list[str], 
                  cat_cols: list[str]) -> pd.DataFrame:
    """
    Fills missing values using mean for numeric and mode for categorical columns.

    Args:
        df (pd.DataFrame): The DataFrame containing null values.
        num_cols (list[str]): List of numeric columns to impute with mean.
        cat_cols (list[str]): List of categorical columns to impute with mode.

    Returns:
        pd.DataFrame: DataFrame with no remaining missing values in specified columns.
    """
    logger.info("Imputing missing values.")
    for col in [c for c in num_cols if c in df.columns]:
        df[col] = df[col].fillna(df[col].mean())
    
    for col in [c for c in cat_cols if c in df.columns]:
        if not df[col].mode().empty:
            df[col] = df[col].fillna(df[col].mode()[0])
    return df

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates new business metrics from existing raw data.

    Args:
        df (pd.DataFrame): The cleaned DataFrame.

    Returns:
        pd.DataFrame: DataFrame with the 'MonthlyChargeRatio' feature added.
    """
    logger.info("Engineering new features.")
    if 'TotalCharges' in df.columns and 'tenure' in df.columns:
        df['MonthlyChargeRatio'] = df['TotalCharges'] / (df['tenure'] + 1)
    return df

def format_target(df: pd.DataFrame, 
                  target: str) -> pd.DataFrame:
    """
    Maps the target string labels to binary integers.

    Args:
        df (pd.DataFrame): The DataFrame containing the target.
        target (str): The name of the target column (e.g., 'Churn').

    Returns:
        pd.DataFrame: DataFrame with a new 'churn_binary' column.
    """
    if target in df.columns:
        logger.info(f"Standardizing target column: {target}")
        df['churn_binary'] = df[target].map({'Yes': 1, 'No': 0})
    return df

def clean_and_enrich_churn_data(
    df: pd.DataFrame, 
    target: str, 
    numeric_cols: list[str], 
    categorical_cols: list[str],
    final_columns: list[str]
) -> pd.DataFrame:
    """
    Cleans data types, imputes missing values, and creates calculated fields.

    Args:
        df (pd.DataFrame): The raw input DataFrame.
        target (str): The name of the original target column.
        numeric_cols (list[str]): List of numeric column names.
        categorical_cols (list[str]): List of categorical column names.
        final_columns (list[str]): The final list of columns to return.

    Returns:
        pd.DataFrame: A cleaned and enriched DataFrame with the specified schema.
    """
    logger.info(f"Starting preprocessing. Input shape: {df.shape}")
    
    # Start with a copy to avoid changing the original data
    df_clean = df.copy()
    
    # Execute steps one by one
    df_clean = handle_types(df_clean)
    df_clean = impute_values(df_clean, numeric_cols, categorical_cols)
    df_clean = add_features(df_clean)
    df_clean = format_target(df_clean, target)
    
    # Select final columns
    result_df = df_clean[final_columns]
    
    logger.info(f"Preprocessing complete. Final shape: {result_df.shape}")
    return result_df

# ==========================================
# SECTION: PIPELINE (The source for pipeline.py)
# ==========================================
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

# ==========================================
# SECTION: MAIN (The source for main.py)
# ==========================================
def main() -> None:
    """
    Orchestrates the pipeline execution by passing configurations to the pipeline function.
    """
    try:
        run_de_pipeline(
            input_path=RAW_DATA_PATH,
            output_path=PROCESSED_DATA_PATH,
            target=TARGET,
            num_cols=NUMERIC_COLS,
            cat_cols=CATEGORICAL_COLS,
            final_cols=COLUMNS_TO_KEEP
        )
        print("Success: Churn pipeline completed!")
        logger.info("Success: Churn pipeline completed!")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        #logging.error(f"Pipeline failed: {e}")

if __name__ == "__main__":
    main()