def getParameters():
    parameters = {}
    parameters['OTP_SESSION_TIME'] = 15  # Minutes
    parameters['TOKEN_EXPIRY_TIME'] = 30  # Minutes
    parameters['MOBILE_NUMBER_DIGITS'] = 10
    parameters['MOBILE_NUMBER_FORMAT'] = "^[0-9]{10}$"
    parameters['OTP_DIGITS'] = 6
    # parameters['JWT_SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
    return parameters
