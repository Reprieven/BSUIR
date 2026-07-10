from typing import List
from element import Element
from copy import deepcopy
def make_combination(n: int):
    combinations = []
    for i in range(n):
        comb = [False]*n
        comb[i] = True
        combinations.append(comb)
    return combinations

def make_nodes(x_all:List[List[Element]]):
    nodes = []
    combs = make_combination(len(x_all[0]))
    for i in range(len(x_all)):
        for comb in combs:
            node = deepcopy(x_all[i])
            for j in range(len(node)):
                node[j].is_constant = comb[j]
                node[j].level = i
            nodes.append(node)     
    return nodes

            
    

