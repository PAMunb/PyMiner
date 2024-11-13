# Decoradores simples (antes da PEP 614)
@decorator_name
def simple_decorator_function():
    pass

@my_decorator
def another_simple_decorator_function():
    pass

# Decoradores com funções
@my_function()
def function_as_decorator():
    pass

@some_function_call('arg')
def function_call_decorator():
    pass

# Decoradores com acesso a atributos ou métodos
class MyClass:
    @some_instance.method()
    def method_with_instance_access(self):
        pass

    @module.decorator
    def method_with_module_access(self):
        pass

# Decoradores com acesso a índices
my_dict = {'key': 'value'}

@my_dict['key']
def decorator_with_dict_access():
    pass

# Decoradores com chamadas e atribuições complexas
@another_module.decorator(attribute='value')
def complex_decorator():
    pass

@lambda x: x * 2
def lambda_as_decorator():
    pass

# Decoradores com operadores e expressões aritméticas
@some_function() + another_function()
def operator_as_decorator():
    pass

# Decoradores com chamadas a funções e operações lógicas
@some_function() and another_function()
def logical_operator_decorator():
    pass

# Decoradores complexos usando expressões em listas
@['decorator', 'list'][1]
def decorator_from_list():
    pass

# Decoradores com expressões ternárias
@('cond' if True else 'default')
def ternary_expression_decorator():
    pass

# Decoradores utilizando a definição do tipo
@type(3)
def type_expression_decorator():
    pass
