import random

BITS = 1024

def is_prime(num, k = 20):
    if num == 2 or num == 3:
        return True
    if num % 2 == 0:
        return False
    n = num
    d = n - 1
    s = 0

    while d%2 == 0:
        d//=2
        s+=1
    
    for _ in range(k):
        a = random.randint(2, n-2)
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue

        for _ in range(s-1):
            x = pow(x, 2, n)
            if x == n-1:
                break
        else:
            return False
    return True


def generate_prime_number():
    while True:
        x = random.getrandbits(BITS)
        if is_prime(x):
            return x
        