from matrix import Matrix
from element import Element
def find_x(y_set: dict, matrix: Matrix):
    val_matrix = matrix.values
    vars = matrix.vars
    elem_all = []
    y_values = list(y_set.values())
    for i in range(len(val_matrix)):
        elem_lvl = []
        y = y_values[i]
        for j in range(len(val_matrix[0])):
            x = 1+y-val_matrix[i][j]
            elem = Element(vars[j], x)
            elem_lvl.append(elem)
        elem_all.append(elem_lvl)
    return elem_all


