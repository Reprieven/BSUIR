import string
import random
def generate_string(length: int)->str:
    symbols = list(string.ascii_letters)+list(string.digits)
    password = random.choices(symbols, k = length)
    password_str = ''.join(password)
    return password_str

def choose_password(string: str, start: int, length: int)->str:
    return string[start:start+length]
