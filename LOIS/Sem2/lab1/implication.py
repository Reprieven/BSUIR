##############################################################
# Лабораторная работа 1 по дисциплине ЛОИС
# Выполнено студентами группы 321701 БГУИР
# Климков Марат Петрович
# Бедарик Захар Александрович
# Гринь Роман Алексеевич
# Файл реализации построения матрицы
# 17.10.2025
##############################################################
def make_matrix_implication(first:str, second: str):
    first_values = list(first.values())
    second_values = list(second.values())
    result_matrix = []
    for b in second_values:
        row = []
        for a in first_values:
            if a <= b:
                row.append(1)
            else:
                row.append(1+b-a)
        result_matrix.append(row)
    print(result_matrix)
    return result_matrix