# Exemplo 1: Desempacotamento de lista
a, *b, c = [1, 2, 3, 4, 5]
print(f"a={a}, b={b}, c={c}")  # a=1, b=[2, 3, 4], c=5

# Exemplo 2: Desempacotamento em funções
def unpacking_func(*args):
    first, *rest = args
    print(f"first={first}, rest={rest}")

unpacking_func(1, 2, 3, 4)  # first=1, rest=[2, 3, 4]

# Exemplo 3: Desempacotamento em tuplas
x, *y, z = (10, 20, 30, 40, 50)
print(f"x={x}, y={y}, z={z}")  # x=10, y=[20, 30, 40], z=50

# Exemplo 4: Desempacotamento em string
a, *b, c = "hello"
print(f"a={a}, b={b}, c={c}")  # a=h, b=['e', 'l', 'l'], c=o

# Exemplo 5: Desempacotamento em dicionário
data = {'name': 'Alice', 'age': 30, 'city': 'Wonderland'}
name, *_, age = data.values()
print(f"name={name}, age={age}")  # name=Alice, age=30