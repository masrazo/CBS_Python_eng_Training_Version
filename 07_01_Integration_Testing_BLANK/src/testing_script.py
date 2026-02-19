###Testing:
import config
from data_loader import extract_from_csv
from preprocessing import clean_and_enrich_churn_data
from pipeline import run_de_pipeline

raw_df=extract_from_csv(config.RAW_DATA_PATH)
#output_path=config.PROCESSED_DATA_PATH,
target=config.TARGET
num_cols=config.NUMERIC_COLS
cat_cols=config.CATEGORICAL_COLS
final_cols=config.COLUMNS_TO_KEEP

#print(type(raw_df))

"""clean_and_enrich_churn_data(
        df=raw_df,
        target=target,
        numeric_cols=num_cols,
        categorical_cols=cat_cols,
        final_columns=final_cols
    )"""

run_de_pipeline(
            input_path=config.RAW_DATA_PATH,
            output_path=config.PROCESSED_DATA_PATH,
            target=config.TARGET,
            num_cols=config.NUMERIC_COLS,
            cat_cols=config.CATEGORICAL_COLS,
            final_cols=config.COLUMNS_TO_KEEP
        )