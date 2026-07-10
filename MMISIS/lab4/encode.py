from find_g import find_g

def encode(P, exponent):
    g = find_g(P)
    return pow(g, exponent, P)

def get_key(P, exponent, other_person_value): 
    return pow(other_person_value, exponent, P)
