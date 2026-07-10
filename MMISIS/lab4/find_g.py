import numpy as np

def find_factors(P: int) -> set:
    n = P - 1
    P_temp = n
    i = 2
    factors = set()
    while i * i <= P_temp:
        while P_temp % i == 0:
            factors.add(i)
            P_temp //= i
        i += 1

    if P_temp > 1:
        factors.add(P_temp)
    
    return factors

def find_g(P: int)->int:
    factors = find_factors(P)
    P_temp = P-1
    for g in range(2, P-1):
        is_root = True
        for f in factors:
            exponent = P_temp // f
            if pow(g, exponent, P) == 1:
                is_root = False
                break
        if is_root:
            return g
    return -1

