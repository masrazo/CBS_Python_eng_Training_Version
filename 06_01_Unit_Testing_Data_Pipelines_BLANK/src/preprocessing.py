"""
src/preprocessing.py
Responsible for the 'Transform' phase, including cleaning and enrichment.
"""
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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