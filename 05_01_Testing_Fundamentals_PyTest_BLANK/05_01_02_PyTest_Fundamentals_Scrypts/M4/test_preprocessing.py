# test_preprocessing.py
import pytest
import pandas as pd
import numpy as np
from preprocessing import (
                            convert_price_column, fill_missing_prices,
                            add_total_column, categorise_order_size
                            )

# --- Type conversion tests ---


### Exercise 4.1: Write Your Own Tests

#Given the functions on preprocessing.py, write tests for:

#1. What happens when `add_total_column` receives a DataFrame where `quantity` is zero?
#2. What happens when `convert_price_column` receives a DataFrame where ALL prices are valid numbers? (No NaN should be created.)
#3. Does `categorise_order_size` assign `'Large'` to a quantity of exactly `11`?