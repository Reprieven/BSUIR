from random_1024 import generate_prime_number
def gen_g_p():
    g = generate_prime_number()
    while True:
        p = generate_prime_number()
        if g!=p:
            return g, p
        
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = extended_gcd(b,a%b)
        return d, y, x-y*(a//b)

def gen_dexp(exp, euler):
    gcd, x, y = extended_gcd(exp, euler)
    if gcd != 1:
        raise ValueError('Числа не являются взаимно простыми')
    d = x % euler
    return d

def gen_keys():
    g, p = gen_g_p()
    n = g*p
    euler = (g-1)*(p-1)
    exp = 65537
    dexp = gen_dexp(exp, euler)
    keys = ((exp, n), (dexp, n))
    return keys


