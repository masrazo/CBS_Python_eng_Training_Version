# test_helpers.py
from helpers import add

def test_add_positive_numbers():
    # ARRANGE: Set up inputs
    a = 3
    b = 7

    # ACT: Call the function
    result = add(a, b)

    # ASSERT: Check the output
    assert result == 10

def test_add_negative_numbers():
    # ARRANGE: Set up inputs
    a = -5
    b = -2

    # ACT: Call the function
    result = add(a, b)

    # ASSERT: Check the output
    assert result == -7

def test_add_zero():
    # ARRANGE: Set up inputs
    a = 0
    b = 0
# ACT: Call the function
    result = add(a, b)

    # ASSERT: Check the output
    assert result == 0


def test_integer_string():
    # ARRANGE: Set up inputs
    a = 5
    b = "a"
# ACT: Call the function
    result = add(a, b)

    # ASSERT: Check the output
    assert result == 0

