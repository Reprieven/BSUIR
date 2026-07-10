from typing import List
def decode_scytale(encoded_message: str, rows: int, cols: int)->str:
    matrix = [['' for _ in range(cols)] for _ in range(rows)]
    decoded = ''
    current_row = 0
    current_col = 0
    for ch in encoded_message:
        if current_row == rows:
            current_row = 0
            current_col+=1
        if current_col == cols:
            break
        matrix[current_row][current_col] = ch
        current_row+=1
    for i in range(rows):
        for j in range(cols):
            decoded += matrix[i][j]
    return decoded
