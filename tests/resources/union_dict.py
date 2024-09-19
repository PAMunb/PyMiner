dict1 = {'a': 1}
dict2 = {'b': 2}
result = dict1 | dict2

dict1 |= dict2

a = 1 | 2  # Operação bitwise comum
b = 3
b |= 4

dict1 = {'a': 1}
dict2 = {'b': 2}
result = dict1 & dict2  # Operação inválida
dict1 += dict2  # Não é a operação da PEP 584