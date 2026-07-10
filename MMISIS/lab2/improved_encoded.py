from typing import List
from random import choice
from improve_decoded import decode_with_key
def encode_with_key(message: str, rows: int, cols: int, key:List[int] )->str:
    russian_lower = [chr(i) for i in range(1072, 1104)]
    if len(message) < (rows*cols):
        diff = (rows*cols) - len(message)
        for i in range(diff):
            message+=choice(russian_lower)
    matrix = [[] for _ in range(rows)]
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
    reshuffled_matrix = [[] for _ in range(rows)]
    for col_index in key:
        for i in range(rows):
            reshuffled_matrix[i].append(matrix[i][col_index])
    for j in range(cols):
        for i in range(rows):
            encoded+=reshuffled_matrix[i][j]
    return encoded

