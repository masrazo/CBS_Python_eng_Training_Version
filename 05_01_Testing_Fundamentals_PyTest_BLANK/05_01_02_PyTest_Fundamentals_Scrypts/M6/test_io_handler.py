# test_io_handler.py

import pytest
import os
import pandas as pd
from io_handler import load_csv, save_to_csv

def test_load_csv_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_csv("this/path/does/not/exist.csv")

def test_load_csv_error_message():
    with pytest.raises(FileNotFoundError, match="File not found"):
        load_csv("fake_data.csv")


# test_io_handler.py (continued)

def test_save_creates_file(tmp_path):
    """tmp_path gives us a safe temporary directory."""
    df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    output_file = tmp_path / "output" / "results.csv"

    save_to_csv(df, str(output_file))

    assert os.path.exists(output_file)

def test_save_and_reload_integrity(tmp_path):
    """Write → Read → Compare. Data should survive the round trip."""
    df = pd.DataFrame({'name': ['Alice', 'Bob'], 'score': [95, 82]})
    filepath = tmp_path / "round_trip.csv"

    save_to_csv(df, str(filepath))
    loaded = pd.read_csv(filepath)

    assert len(loaded) == 2
    assert list(loaded.columns) == ['name', 'score']
    assert loaded['name'][0] == 'Alice'