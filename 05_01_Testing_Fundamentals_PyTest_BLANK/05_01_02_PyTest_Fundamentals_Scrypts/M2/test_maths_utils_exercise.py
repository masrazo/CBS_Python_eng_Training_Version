#Exercise 2.1: Write Your Own Tests

#for math_utils.py Write tests for:
#1. `multiply(4, 5)` should return `20`
#2. `multiply(-3, 3)` should return `-9`
#3. `multiply(anything, 0)` should return `0`
#4. `is_even(4)` should be `True`
#5. `is_even(7)` should be `False`

##Your code:

from maths_utils import multiply, is_even
 
def test_multiply_positive_value():
    # arrange:
    a = 4
    b = 5
    # act:
    result = multiply(a, b)
    # assert:
    assert result == 20
 
 
def test_multiply_negative_value():
    # arrange
    a = -3
    b = 3
    # act
    result = multiply(a ,b)
    # assert
    assert result == -9
 
 
def test_multiply_by_zero():
    # arrange:
    a = 4
    b = 0
    # act:
    result = multiply(a, b)
    # assert:
    assert result == 0
 
 
def test_is_even():
    # arrange:
    number = 4
    # act:
    result = is_even(number)
    # assert:
    assert result == True
 
 
def test_is_odd():
    # arrange:
    number = 7
    # act:
    result = is_even(number)
    # assert:
    assert result == False
 