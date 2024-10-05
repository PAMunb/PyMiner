# Exemplo 1: Unpacking em listas
lista1 = [1, 2, 3]
lista2 = [4, 5, 6]
combined_list = [*lista1, *lista2]
print("Lista combinada:", combined_list)

# Exemplo 2: Unpacking em tuplas
tupla1 = (7, 8, 9)
tupla2 = (10, 11, 12)
combined_tuple = (*tupla1, *tupla2)
print("Tupla combinada:", combined_tuple)

# Exemplo 3: Unpacking em sets
set1 = {13, 14, 15}
set2 = {16, 17, 18}
combined_set = {*set1, *set2}
print("Set combinado:", combined_set)

# Exemplo 4: Unpacking em dicionários
dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3, 'd': 4}
combined_dict = {**dict1, **dict2}
print("Dicionário combinado:", combined_dict)

# Exemplo 5: Unpacking misturado em uma lista
mixed_combined = [0, *range(1, 4), 5, *lista1]
print("Combinado misto em lista:", mixed_combined)

# Exemplo 6: Unpacking com argumentos de função
def func(x, y, z):
    return x + y + z

args = [1, 2, 3]
print("Resultado de função com args:", func(*args))

# Exemplo 7: Unpacking com argumentos nomeados
def func_kwarg(a, b, c):
    return f"a={a}, b={b}, c={c}"

kwargs = {'a': 10, 'b': 20, 'c': 30}
print("Resultado de função com kwargs:", func_kwarg(**kwargs))

# Exemplo 8: Unpacking aninhado em listas e tuplas
lista3 = [*lista1, (*tupla1, 19, 20), *set1]
print("Lista aninhada com unpacking:", lista3)

# Exemplo 9: Unpacking de dicionários misturados com outros elementos
dict3 = {'e': 5, 'f': 6}
dict_combined_with_literal = {**dict1, 'x': 100, **dict3}
print("Dicionário com literal e unpacking:", dict_combined_with_literal)

# Exemplo 10: Unpacking de argumentos em funções de várias fontes
def func_args(*args):
    return sum(args)

more_args = (4, 5, 6)
print("Soma com args de múltiplas fontes:", func_args(*args, *more_args))

# Exemplo 11: Combinação de desempacotamento em uma compreensão de lista
listas_combinadas = [x for x in [*lista1, *lista2, *tupla1] if x % 2 == 0]
print("Compreensão de lista com desempacotamento:", listas_combinadas)

# Exemplo 12: Usando desempacotamento em chamadas de método de instância
class Exemplo:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

args = (1, 2, 3)
obj = Exemplo(*args)
print(f"Objeto instanciado com unpacking: a={obj.a}, b={obj.b}, c={obj.c}")

# Exemplo 13: Unpacking com valores padrão em chamadas de função
def func_com_default(x, y=0, z=0):
    return f"x={x}, y={y}, z={z}"

print("Função com desempacotamento e valores padrão:", func_com_default(1, *args[1:]))

# Exemplo 14: Desempacotamento dentro de um `print` (direct use)
print("Diretamente com desempacotamento:", *[1, 2, 3], *{4, 5, 6})
