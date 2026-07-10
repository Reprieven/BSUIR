import random
from typing import List

def encode_scytale(message: str, rows: int, cols: int)->str:
    russian_lower = [chr(i) for i in range(1072, 1104)]
    if len(message) < (rows*cols):
        diff = (rows*cols) - len(message)
        for i in range(diff):
            message+=random.choice(russian_lower)
    matrix = [[] for i in range(rows)]
    encoded = ''
    current_col = 0 
    current_row = 0
    for ch in message:
        if current_col == cols:
            current_col = 0
            current_row+=1
        if current_row == rows:
            break
        matrix[current_row].append(ch)
        current_col+=1
    for j in range(cols):
        for i in range(rows):
            encoded+=matrix[i][j]
    return encoded