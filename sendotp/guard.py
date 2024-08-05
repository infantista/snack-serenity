import re
from config import getParameters

parameters = getParameters()

def validate_mobile_no(mobile_number):
    """
    Method will validate the supplied mobile number using regex
    to find any irrelevant characters exist.
    Input arg: mobile number (String)
    Return: Boolean 
    """
    try:
        if re.fullmatch(parameters['MOBILE_NUMBER_FORMAT'], mobile_number):
            return True
        return False
    except Exception as error:
        print(f"Error in validating mobile number: {str(error)}")
        return False
