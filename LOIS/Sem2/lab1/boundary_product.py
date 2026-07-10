##############################################################
# Лабораторная работа 1 по дисциплине ЛОИС
# Выполнено студентами группы 321701 БГУИР
# Климков Марат Петрович
# Бедарик Захар Александрович
# Гринь Роман Алексеевич
# Файл реализации формулы граничного произведения 
# 17.10.2025
##############################################################
from rule_maker import ImplementedRule

def make_boundary_product(rule: ImplementedRule, third_set: dict):
        result_matrix = []
        third_values = list(third_set.values())
        for y in range(len(rule.matrix)):
            row = []
            for x in range(len(rule.matrix[0])):
                new_x = third_values[x]
                row.append(max(new_x + rule.matrix[y][x]-1, 0)) 
            result_matrix.append(row)
        y_values = [max(y) for y in result_matrix]
        y_keys = list(rule.second_set.keys())
        return dict(zip(y_keys, y_values))