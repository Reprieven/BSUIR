from decoder import decode_scytale
from typing import List
import string

def divisors(num: int):
    divisors = set()
    for i in range(1,num):
        if num % i == 0:
            divisors.add(i)
            divisors.add(num//i)
    return sorted(divisors)

def attack_simulation(encoded: str):
    n = len(encoded)
    for parts in divisors(n):
        chunk_len = n // parts

        chunks = [encoded[i*chunk_len:(i+1)*chunk_len] for i in range(parts)]

        for rows in divisors(chunk_len):
            cols = chunk_len // rows 
            candidate = ''.join(decode_scytale(ch, rows, cols) for ch in chunks)
            print(candidate)
            answer = input('Имеет ли текст какой-то смысл? (y/n) ')
            if answer.lower().startswith('y'):
                return f'Таблиц {parts}, количество строк таблицы {rows}, количество столбцов таблицы {cols}'
    
    return 'Подходящие параметры не найдены'
            
                
