##############################################################
# Лабораторная работа 1 по дисциплине ЛОИС
# Выполнено студентами группы 321701 БГУИР
# Климков Марат Петрович
# Бедарик Захар Александрович
# Гринь Роман Алексеевич
# Главный файл программы
# Вариант 3
# 17.10.2025
##############################################################
from find_results import find_results, round_results
from parser import *


if __name__ == "__main__":
    try:
        with open("1.txt", "r", encoding="utf-8") as f:
            text = f.read()
        tree = parser.parse(text)
        sets, rules = extract(tree)
        results, made_operations = find_results(sets, rules)
        for i, result in enumerate(results):
            fuzzy_input = made_operations[i][0]
            condition = made_operations[i][1]
            conclusion  = made_operations[i][2]
            round_result = round_results(result)
            items = [f"<{key}, {value}>" for key, value in round_result.items()]
            clean_result = "{" + ",  ".join(items) + "}"
            print(f'{{{fuzzy_input}, {condition}(x)~>{conclusion}(y)}} |~ _{i}={clean_result}')
    except Exception as e:
        print('Error: Неправильный формат исходных данных')
 
