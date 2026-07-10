import re

def check_range(value, name):
    if not (0.0 <= value <= 1.0):
        raise ValueError(f"Value {value} in {name} is out of range [0.0, 1.0]")

def parse_data(filename):
    with open(filename, 'r') as file:
        data = file.read()
    b_match = re.search(r"C=\{(.*?)\}", data, re.DOTALL)
    if b_match:
        b_content = b_match.group(1).strip()
        matches = re.findall(r"<(y\d+),\s*([\d.]+)>", b_content)
        C = {}
        for key, value in matches:
            value = float(value)
            check_range(value, f"C[{key}]")
            C[key] = value
    else:
        C = {}

    l_match = re.search(r"A=\(([\s\S]*?)\)", data)
    if l_match:
        l_content = l_match.group(1).strip()
        l_rows = l_content.split('\n')
        A = []
        first_row = True
        num_cols = None
        
        for i, row in enumerate(l_rows):
            row = row.strip()
            if not row:
                continue
            if first_row:
                headers = row.split()
                if len(headers) != len(set(headers)):
                    raise ValueError(f"Duplicate headers found in A: {headers}")
                A.append(headers)
                num_cols = len(headers)
                first_row = False
                continue
            
            row_values = row.split()
            if len(row_values) != num_cols:
                raise ValueError(f"Row {len(A)} has {len(row_values)} values, expected {num_cols}: {row}")
            
            try:
                row_values = list(map(float, row_values))
                for j, value in enumerate(row_values):
                    check_range(value, f"A[{len(A)}][{j}]")
                A.append(row_values)
            except ValueError as e:
                raise ValueError(f"Invalid number in row {len(A)}: {row}")
    else:
        A = []

    if len(C) != len(A)-1:
        raise ValueError(f"len(C) != len(A)")


    return C, A