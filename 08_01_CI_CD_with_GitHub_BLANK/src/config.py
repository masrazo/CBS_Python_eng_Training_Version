"""
src/config.py
Contains all configuration constants, column definitions, and file paths.
"""
from pathlib import Path
import pandas as pd
# Column definitions
TARGET: str = 'Churn'

NUMERIC_COLS: list[str] = ['tenure', 'MonthlyCharges', 'TotalCharges']

CATEGORICAL_COLS: list[str] = [
    'gender', 'SeniorCitizen', 'Partner', 'Dependents', 
    'PhoneService', 'MultipleLines', 'InternetService'
]

# The final schema for the "Gold" table (Analytics/Modeling ready)
COLUMNS_TO_KEEP: list[str] = NUMERIC_COLS + CATEGORICAL_COLS + ['MonthlyChargeRatio', 'churn_binary']

#Root path:
project_root = Path(__file__).resolve().parent.parent

# File Paths
##Data sources
#INPUT_DATA_PATH: str = "data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv"
#RAW_DATA_PATH = project_root / INPUT_DATA_PATH
RAW_DATA_PATH = "https://rockborne-bucket-01-cbs.s3.eu-west-2.amazonaws.com/DataSources/WA_Fn-UseC_-Telco-Customer-Churn.csv"
##Pre-process data path
CLEAN_DATA_PATH: str = "data/processed/churn_preprocessed.csv"
PROCESSED_DATA_PATH = project_root / CLEAN_DATA_PATH