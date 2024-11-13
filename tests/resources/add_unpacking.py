# Exemplos para serem capturados pelo UnpackVisitor

# 1. Desempacotamento em atribuição (PEP 3132)
a, b, *rest = [1, 2, 3, 4]          # Deve ser capturado como 'assign_unpack'
*beginning, end = (1, 2, 3, 4)      # Deve ser capturado como 'assign_unpack'

x, y, *middle, z = (1, 2, 3, 4, 5)  # Capturado como 'assign_unpack'
first, *rest = {'key1': 'value1', 'key2': 'value2'}  # Capturado como 'assign_unpack'

# 2. Desempacotamento em listas, tuplas e conjuntos (PEP 448)
list_example = [1, *[2, 3], 4]      # Deve ser capturado como 'list_unpack'
tuple_example = (1, *[2, 3], 4)     # Deve ser capturado como 'tuple_unpack'
set_example = {1, *{2, 3}, 4}       # Deve ser capturado como 'set_unpack'

# 3. Desempacotamento em dicionário (PEP 448)
dict_example = {**{'a': 1, 'b': 2}, 'c': 3}  # Deve ser capturado como 'dict_unpack'

# 4. Desempacotamento em argumentos de chamadas de função (PEP 448)
def example_func(a, b, c):
    pass

example_func(1, *[2, 3])           # Deve ser capturado como 'call_args_unpack'
example_func(**{'a': 1, 'b': 2, 'c': 3})  # Deve ser capturado como 'call_kwargs_unpack'

# Exemplos para serem ignorados pelo UnpackVisitor

# Desempacotamento padrão em variáveis sem uso de *
a, b, c = [1, 2, 3]               # Deve ser ignorado

# Criação de listas, tuplas e conjuntos normais, sem desempacotamento
normal_list = [1, 2, 3, 4]        # Deve ser ignorado
normal_tuple = (1, 2, 3, 4)       # Deve ser ignorado
normal_set = {1, 2, 3, 4}         # Deve ser ignorado

# Criação de dicionário normal, sem desempacotamento
normal_dict = {'a': 1, 'b': 2}    # Deve ser ignorado

# Chamadas de função sem desempacotamento
example_func(1, 2, 3)             # Deve ser ignorado
example_func(a=1, b=2, c=3)       # Deve ser ignorado