from itertools import product
from generator import generate_string, choose_password
import string
import time

def brute_force(password):
    symbols = list(string.ascii_letters)+list(string.digits)
    length = len(password)
    for combination in product(symbols, repeat=length):
        if combination == password:
            return True
    return False

def bruteforce_count_time(password):
    timespans = []
    for i in range(1,len(password)+1):
        start = time.perf_counter()
        brute_force(password[0:i])
        end = time.perf_counter()
        timespans.append(end-start)
    timer = 0
    for elem in timespans:
        timer+=elem
    print(timer, 'сек')
    return timespans

