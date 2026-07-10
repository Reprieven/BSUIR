##############################################################
# Лабораторная работа 1 по дисциплине ЛОИС
# Выполнено студентами группы 321701 БГУИР
# Климков Марат Петрович
# Бедарик Захар Александрович
# Гринь Роман Алексеевич
# Файл находящий результаты
# 17.10.2025
##############################################################
from rule_maker import ImplementedRule
from boundary_product import make_boundary_product
def find_results(sets, rules):
    made_operations = []
    implemented = []
    set_names = list(sets.keys())
    for rule in rules:
        first_set_name = rule[0]
        first_set = sets[first_set_name]
        second_set_name = rule[1]
        second_set = sets[second_set_name]
        implemented_rule = ImplementedRule(first_set_name, first_set, second_set_name, second_set)
        implemented.append(implemented_rule)

    first_order_results = []
    for rule in implemented:
        for name in set_names:
            if (sorted(list(rule.first_set.keys())) == sorted(list(sets[name].keys()))) and \
            (name, rule.first_set_name, rule.second_set_name) not in made_operations:
                new_set = make_boundary_product(rule, sets[name])
                first_order_results.append(new_set)
                made_operations.append((name, rule.first_set_name, rule.second_set_name))  
    second_order_results = []
    for i, result_set in enumerate(first_order_results):
        result_name = f"_{i}"
        for rule in implemented:
            if (sorted(list(rule.first_set.keys())) == sorted(list(result_set.keys()))) and \
            (result_name, rule.first_set_name, rule.second_set_name) not in made_operations:
                new_set = make_boundary_product(rule, result_set)
                second_order_results.append(new_set)
                made_operations.append((result_name, rule.first_set_name, rule.second_set_name))
    results = first_order_results+second_order_results
    return results, made_operations

def round_results(result_set, decimals=6):
    return {key: round(value, decimals) for key, value in result_set.items()}