##############################################################
# Лабораторная работа 1 по дисциплине ЛОИС
# Выполнено студентами группы 321701 БГУИР
# Климков Марат Петрович
# Бедарик Захар Александрович
# Гринь Роман Алексеевич
# Файл реализации класса отношения  
# 17.10.2025
##############################################################
from implication import make_matrix_implication
class ImplementedRule:
    def __init__(self,first_set_name, first_set, second_set_name, second_set):
        self.first_set_name = first_set_name
        self.second_set_name = second_set_name
        self.first_set = first_set
        self.second_set = second_set
        self.matrix = make_matrix_implication(first_set, second_set)