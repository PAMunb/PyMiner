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


def func(a, b, c):
    print(a, b, c)

args = (1, 2, 3)
kwargs = {'a': 1, 'b': 2, 'c': 3}

func(*args)     # ✅ Válido antes da PEP 448
func(**kwargs)  # ✅ Válido antes da PEP 448


class MinhaClasse:
    def __init__(self, *args, **kwargs):
        self.data = args
        self.options = kwargs

obj = MinhaClasse(1, 2, x=10, y=20)


def soma(a, b, c):
    return a + b + c

valores = [1, 2, 3]
soma(*valores)  # ✅ Válido antes da PEP 448

def chama_funcao(*args):
    outra_funcao(*args)  # ✅ Isso sempre foi permitido!
    
    
# ✅ Captura múltiplos desempacotamentos de listas (PEP 448)
example_func(*[1, 2], *[3, 4])  # -> call_args_unpack

# ✅ Captura múltiplos desempacotamentos de dicionários (PEP 448)
example_func(**{'a': 1}, **{'b': 2})  # -> call_kwargs_unpack

# ✅ Captura desempacotamento único de literal (PEP 448)
example_func(*[1, 2, 3])  # -> call_args_unpack
example_func(**{'a': 1, 'b': 2})  # -> call_kwargs_unpack

# testes a serem ignorados - Marcos

import numpy as np

def _check_ninf_nan(dummy):
            msgform = "cexp(-inf, nan) is (%f, %f), expected (+-0, +-0)"
            err = np.seterr(invalid='ignore')
            try:
                z = f(np.array(np.complex(-np.inf, np.nan)))
                if z.real != 0 or z.imag != 0:
                    raise AssertionError(msgform % (z.real, z.imag))
            finally:
                np.seterr(**err)
                
                
np.seterr(**olderr)


self.process_token(*token)


def rand(*args):
    if isinstance(args[0], tuple):
        args = args[0]
    return asmatrix(np.random.rand(*args))

result = getattr(asarray(obj),method)(*args, **kwds)

self.build_library_sources(*libname_info)


self.path_in_package = os.path.join(*self.name.split('.'))

def random(size):
    return rand(*size)