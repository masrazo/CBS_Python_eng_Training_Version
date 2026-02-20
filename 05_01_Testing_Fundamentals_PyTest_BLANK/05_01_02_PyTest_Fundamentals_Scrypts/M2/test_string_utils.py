# test_string_utils.py
from string_utils import clean_name, is_valid_email, calculate_discount

def test_clean_name_string_whitespace():
    #Arrange
    test_text = "    miguel razo    "
    #Act
    result = clean_name(test_text)
    #Assert
    assert result == "Miguel Razo"

def test_clean_name_title_case():
    #Arrange
    test_text = "    miguel RAZO    "
    #Act
    result = clean_name(test_text)
    #Assert
    assert result == "Miguel Razo"

def test_valie_email_valid():
    #Arrange
    test_email = "user@example.com"
    #Act
    result = is_valid_email(test_email)
    #Assert
    assert result == True
    #Assert

def test_invalid_email():
    #Arrange
    test_email = "user@examplecom"
    #Act
    result = is_valid_email(test_email)
    #Assert
    assert result == False
    #Assert
