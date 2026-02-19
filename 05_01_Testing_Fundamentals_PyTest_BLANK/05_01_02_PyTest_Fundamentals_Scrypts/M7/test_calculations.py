# test_calculations.py
import pytest
from calculations import calculate_charge_ratio, apply_tax, compute_average

def test_charge_ratio():
    result = calculate_charge_ratio(29.85, 1)
    assert result == pytest.approx(14.925)

