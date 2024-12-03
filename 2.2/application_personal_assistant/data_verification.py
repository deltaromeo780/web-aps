import re
from datetime import datetime

def phone_verification(phone_number):
    
        pattern = re.compile(r'^(\+\d{1,3}\s?)?(\d{3}-\d{3}-\d{3}|\d{9,12})$') #phone number pattern, e.g. +48123456789, 123-456-789, 963852741
        result = bool(pattern.match(str(phone_number))) # if nuber is in patter return True otherwise False
        return result
    
     
def email_verification(email):
    
        pattern = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9._]+@[a-zA-Z0-9]+\.[a-zA-Z][a-zA-Z]+$')
        result = bool(pattern.match(str(email)))
        return result
    

def birthday_verification(birthday):
    try:
        
        datetime.strptime(str(birthday), '%Y-%m-%d')
        return True
    
    except ValueError:
        return False

def result_verification(contact):
    phone_result = DataVerification.phone_verification(contact)
    email_result = DataVerification.email_verification(contact)
    birthday_result = DataVerification.birthday_verification(contact)
    results = {"phone":phone_result, "email":email_result, "birthday":birthday_result}
    return results
