##############################################################
# Лабораторная работа 1 по дисциплине ЛОИС
# Выполнено студентами группы 321701 БГУИР
# Климков Марат Петрович
# Бедарик Захар Александрович
# Гринь Роман Алексеевич
# Файл парсера 
# 17.10.2025
##############################################################
from lark import Lark

with open('grammar.txt','r') as file:
    grammar = file.read()

parser = Lark(grammar, parser='lalr')

def extract(tree):
    sets = {}
    rules = []

    for line in tree.children:
        content = line.children[0]

        if content.data == "assignment":
            name = content.children[0].value
            pair_list = content.children[1]
            result = {}

            for pair in pair_list.children:
                el = pair.children[0].value
                val = float(pair.children[1].value)

                if el not in result:
                    result[el] = val
                else:
                    raise ValueError
            sets[name] = result

        elif content.data == "implication":
            a = content.children[0].value
            b = content.children[1].value
            rules.append((a, b))
    return sets, rules