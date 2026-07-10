from typing import List
from element import Element

def can_combine(first_node: List[Element], second_node: List[Element]) -> bool:
    if len(first_node) != len(second_node):
        return False
    
    for f, s in zip(first_node, second_node):
        if f.is_constant and s.is_constant:
            if f.value != s.value:
                return False
        elif f.is_constant and f.value > s.value:
            return False
        elif s.is_constant and f.value < s.value:
            return False
    return True

def combine_nodes(first_node: List[Element], second_node: List[Element]) -> List[Element]:
    result_node = []
    if first_node[0].level+1 == second_node[0].level and can_combine(first_node, second_node):
        for i in range(len(first_node)):
            name = first_node[i].name
            value = min(first_node[i].value, second_node[i].value)
            elem = Element(name, value)
            elem.level = max(first_node[i].level, second_node[i].level)
            elem.is_constant = first_node[i].is_constant or second_node[i].is_constant
            result_node.append(elem)
    return result_node

def solve_tree(nodes: List[List[Element]]):
    if not nodes:
        return []
    max_lvl = max(node[0].level for node in nodes)
    current_lvl = 0
    levels = {}
    for node in nodes:
        lvl = node[0].level
        if lvl not in levels:
            levels[lvl] = []
        levels[lvl].append(node)
    current_nodes = levels.get(0, [])
    while current_lvl < max_lvl and current_nodes:
        next_lvl = current_lvl + 1
        next_level_nodes = levels.get(next_lvl, [])
        
        new_nodes = []
        
        for current_node in current_nodes:
            for next_node in next_level_nodes:
                if can_combine(current_node, next_node):
                    combined_node = combine_nodes(current_node, next_node)
                    new_nodes.append(combined_node)

        current_nodes = new_nodes
        current_lvl = next_lvl
    res = []
    for i, node in enumerate(current_nodes):
        flag = True
        for elem in node:
            if not (0 <= elem.value <= 1):
                flag = False
        if flag:
           res.append(node) 
            
    return res



            