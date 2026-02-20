from pathlib import Path
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