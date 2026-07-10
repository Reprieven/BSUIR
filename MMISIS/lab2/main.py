from encoder import encode_scytale
from decoder import decode_scytale
from attack import attack_simulation
from improve_decoded import decode_with_key
from improved_encoded import encode_with_key
from random import shuffle
message = input('Введите строку для кодирования: ')
message = message.replace(' ', '')
rows = int(input('Введите количество строк матрицы: '))
cols = int(input('Введите количество столбцов матрицы: '))
key = [i for i in range(cols)]
shuffle(key)
if len(message) > (rows*cols):
    encoded_list = []
    decoded_list = []

    encoded_improved_list = []
    decoded_improved_list = []

    encoded_improved = ''
    decoded_improved = ''

    encoded = ''
    decoded = ''
    start = 0
    step = rows*cols
    while start < len(message):
        encoded_list.append(encode_scytale(message[start:start+step], rows, cols))
        encoded_improved_list.append(encode_with_key(message[start:start+step], rows, cols, key))
        start+=step
    for elem in encoded_list:
        encoded+=elem
        decoded_list.append(decode_scytale(elem, rows, cols)) 
    for elem in encoded_improved_list:
        encoded_improved+=elem
        decoded_improved_list.append(decode_with_key(elem, rows, cols, key))
    for elem in decoded_list:
        decoded+=elem
    for elem in decoded_improved_list:
        decoded_improved+=elem

else:    
    encoded = encode_scytale(message = message, rows = rows, cols = cols)
    decoded = decode_scytale(encoded, rows, cols)
    encoded_improved = encode_with_key(message=message, rows=rows, cols=cols, key = key)
    decoded_improved = decode_with_key(encoded_improved, rows, cols, key)

print(attack_simulation(encoded))

print(f'Закодированное сообщение {encoded}')
print(f'Декодированное сообщение {decoded}')
print('Пример улучшенного алгоритма')
print(f'Закодированное сообщение с улучшенным алгоритмом {encoded_improved}')
print(f'Декодированное сообщение с улучшенным алгоритмом {decoded_improved}')
print('Ключ', key)
