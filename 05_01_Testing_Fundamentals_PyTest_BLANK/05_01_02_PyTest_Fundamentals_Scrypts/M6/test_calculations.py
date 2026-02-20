# test_calculations.py
import pytest
from calculations import divide

def test_divide_normal():
    assert divide(10, 2) == 5.0

def test_divide_by_zero_error():
    with pytest.raises(ValueError):
        divide(10, 0)

def test_divide_by_zero_message():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)



