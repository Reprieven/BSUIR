from parser_data import parse_data
from tree_solver import solve_tree
from x_finder import find_x
from make_tree_nodes import make_nodes
from matrix import Matrix
import os
filename = input("Введите имя файла:")
filename_no_extension = os.path.splitext(filename)[0]
set, matrix = parse_data(filename)
x_all = find_x(set, Matrix(matrix))
nodes = make_nodes(x_all)
solution = solve_tree(nodes)
if not solution:
    print("Нет решений")
else:
    print("Множество С:")
    set_C_elems = [f"<{key},{elem}>" for key, elem in set.items()]
    set_C = '{'+','.join(set_C_elems)+'}'
    print(set_C)

    print("Матрица А:")
    for row in matrix:
        for elem in row:
            print(f"{str(elem):<3}", end=' ')
        print()

    print('Выходные данные программы:')
    B_tuple = '<' + ','.join(f'{filename_no_extension}({elem})' for elem in matrix[0]) + '>'
    node_strings = []
    for node in solution:
        elements_str = ' X '.join(
            '{'+str(round(elem.value, 2))+'}' if elem.is_constant else f'{{[0;{round(elem.value,2)}]}}'
            for elem in node
        )
        node_strings.append(f'({elements_str})')
        
    solution_str = ' ∪ '.join(node_strings) + f' э {B_tuple}'
    print(solution_str)
    





