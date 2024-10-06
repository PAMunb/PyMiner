# Exemplos de dicionários
dict_a = {'a': 1, 'b': 2}
dict_b = {'b': 3, 'c': 4}

# Usando o operador de união
dict_union = dict_a | dict_b
print("Dicionário resultante da união:", dict_union)  # {'a': 1, 'b': 3, 'c': 4}

# Usando o operador de atribuição de união
dict_a |= dict_b
print("Dicionário A após a atribuição de união:", dict_a)  # {'a': 1, 'b': 3, 'c': 4}

# Exemplos adicionais
dict_c = {'d': 5}
dict_d = {'e': 6}

# União de múltiplos dicionários
dict_union_multiple = dict_a | dict_b | dict_c | dict_d
print("União de múltiplos dicionários:", dict_union_multiple)  # {'a': 1, 'b': 3, 'c': 4, 'd': 5, 'e': 6}

# União de dicionários com listas como valores
dict_e = {'f': [1, 2], 'g': [3]}
dict_f = {'f': [4], 'h': [5]}

# União de dicionários com listas (apenas substituição de chaves)
dict_union_lists = dict_e | dict_f
print("União com listas como valores:", dict_union_lists)  # {'f': [4], 'g': [3], 'h': [5]}

# Usando dicionários aninhados
dict_g = {'key1': {'subkey1': 1}, 'key2': 2}
dict_h = {'key1': {'subkey2': 3}, 'key3': 4}

# União de dicionários aninhados (substitui o dicionário aninhado inteiro)
dict_union_nested = dict_g | dict_h
print("União de dicionários aninhados:", dict_union_nested)  # {'key1': {'subkey2': 3}, 'key2': 2, 'key3': 4}

# Operações com valores não-duplicados
dict_i = {'x': 1, 'y': 2}
dict_j = {'y': 3, 'z': 4}

# Atribuição de união e manipulação de valores
dict_i |= dict_j
print("Dicionário I após a atribuição de união:", dict_i)  # {'x': 1, 'y': 3, 'z': 4}

# Utilizando operadores com dicionários vazios
empty_dict = {}
dict_k = {'a': 1, 'b': 2}

# União com dicionário vazio
result_with_empty = empty_dict | dict_k
print("União com dicionário vazio:", result_with_empty)  # {'a': 1, 'b': 2}

# Usando operadores em funções
def merge_dicts(dict1, dict2):
    return dict1 | dict2

merged_result = merge_dicts({'name': 'Alice'}, {'age': 30})
print("Resultado da fusão de dicionários em função:", merged_result)  # {'name': 'Alice', 'age': 30}

######## Exemplos que não devem ser capturados

# Combina dois conjuntos, retornando um novo conjunto que contém todos os elementos únicos de ambos.
set_a = {1, 2, 3}
set_b = {3, 4, 5}
result = set_a | set_b  # {1, 2, 3, 4, 5}

# Realiza uma operação bit a bit de OR entre dois inteiros.

num_a = 5  # 0b0101
num_b = 3  # 0b0011
result = num_a | num_b  # 0b0111 (7)