from typing import List
def decode_with_key(encoded_message: str, rows: int, cols: int, key: List[int]) -> str:
    matrix = [['' for _ in range(cols)] for _ in range(rows)]
    
    current_char_index = 0
    for col_index in key:
        for row in range(rows):
            matrix[row][col_index] = encoded_message[current_char_index]
            current_char_index += 1

    decoded = ''
    for row in matrix:
        decoded += ''.join(row)

    return decoded