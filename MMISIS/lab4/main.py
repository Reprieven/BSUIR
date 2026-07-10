from  encode import encode, get_key
from find_g import find_g
alice_secret = int(input("Введите секретное значение Алисы"))
bob_secret = int(input("Введите секретное значение Боба"))
P = 8699
g = find_g(P)
print(f'Простое число P={P}')
print(f'Первообразный корень g={g}')
encoded_alice = encode(P, alice_secret)
encoded_bob = encode(P, bob_secret)
key_alice = get_key(P, alice_secret, encoded_bob)
key_bob = get_key(P, bob_secret, encoded_alice)
print(f'Закодированное значение Алисы={encoded_alice}')
print(f'Закодированное значение Боба={encoded_bob}')
print(f'Ключ Алисы={key_alice}')
print(f'Ключ Боба={key_bob}')