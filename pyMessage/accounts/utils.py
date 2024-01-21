import re

def parse_phone_number(phone_number):
    if phone_number[0] is '+':
        return phone_number
    return f'+359{phone_number[1:]}'

def is_phone(text):
    return bool(re.match(r'^\+359\d{9}$', text)) or bool(re.match(r'^0\d{9}$', text))
