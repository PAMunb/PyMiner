"""
Arquivo de Teste para Assignment Expressions (Walrus Operator - PEP 572)

Este arquivo contém exemplos válidos de uso do walrus operator em diversas construções:

1. Uso em um if:
   if (n := len(a)) > 10: ...
2. Uso em um while:
   while (line := input()) != "": ...
3. Uso em list comprehension:
   [y := x * 2 for x in range(10)]
4. Uso em dict comprehension:
   {k: (v := k*2) for k in range(5)}
5. Uso em set comprehension:
   {(n := x) for x in range(3)}
6. Uso em generator expression:
   (y := x**2 for x in range(5))
7. Uso aninhado:
   result = (y := (z := 10)) + 5
8. Uso em lambda:
   f = lambda x: (y := x + 1)
9. Uso em expressão condicional:
   a = (b := 2) if (c := True) else (d := 3)
10. Uso em função que retorna uma expressão com walrus:
    def foo(a):
         return (n := a + 1)
11. Uso em laço for (dentro do corpo do loop):
    for _ in range(3):
         print((n := 10))
12. Uso em chamada de função:
    print((x := 5) + 3)

(Observação: o walrus operator foi introduzido no Python 3.8, então este arquivo deve ser executado com Python 3.8 ou superior.)
"""

# 1. Uso em um if
def valid_if(a):
    if (n := len(a)) > 10:
        return n
    return 0

# 2. Uso em um while
def valid_while():
    i = 0
    result = []
    while (line := str(i)) != "5":
        result.append(line)
        i += 1
    return result

# 3. Uso em list comprehension
def valid_list_comprehension():
    return [y := x * 2 for x in range(10)]

# 4. Uso em dict comprehension
def valid_dict_comprehension():
    return {k: (v := k * 2) for k in range(5)}

# 5. Uso em set comprehension
def valid_set_comprehension():
    return {(n := x) for x in range(3)}

# 6. Uso em generator expression
def valid_generator_expression():
    # Convertemos para lista para facilitar a visualização
    return list(y := (x ** 2 for x in range(5)))

# 7. Uso aninhado
def valid_nested():
    result = (y := (z := 10)) + 5
    return result

# 8. Uso em lambda
def valid_lambda():
    f = lambda x: (y := x + 1)
    return f(10)

# 9. Uso em expressão condicional
def valid_conditional():
    a = (b := 2) if (c := True) else (d := 3)
    return a

# 10. Uso em função que retorna uma expressão com walrus
def valid_function_return(a):
    return (n := a + 1)

# 11. Uso em laço for
def valid_for_loop():
    results = []
    for _ in range(3):
        results.append(n := 10)
    return results

# 12. Uso em chamada de função
def valid_function_call():
    # Aqui o valor atribuído é imediatamente usado na chamada de função
    return print((x := 5) + 3)

# --- Casos INVÁLIDOS (sem walrus operator) ---

def invalid_normal_assignment(a):
    # Atribuição padrão, sem walrus operator
    n = len(a)
    if n > 5:
        return n
    return 0

def invalid_for_loop(a):
    result = []
    for x in a:
        result.append(x * 2)
    return result

def invalid_return(a):
    # Apenas retorna o valor, sem assignment expression
    return len(a)

def invalid_lambda():
    # Lambda sem o uso do walrus operator
    f = lambda x: x + 1
    return f(10)

if __name__ == '__main__':
    print("Teste do walrus operator (Assignment Expressions - PEP 572):\n")
    print("valid_if('Hello World!'): ", valid_if("Hello World!"))
    print("valid_while(): ", valid_while())
    print("valid_list_comprehension(): ", valid_list_comprehension())
    print("valid_dict_comprehension(): ", valid_dict_comprehension())
    print("valid_set_comprehension(): ", valid_set_comprehension())
    print("valid_generator_expression(): ", valid_generator_expression())
    print("valid_nested(): ", valid_nested())
    print("valid_lambda(): ", valid_lambda())
    print("valid_conditional(): ", valid_conditional())
    print("valid_function_return(5): ", valid_function_return(5))
    print("valid_for_loop(): ", valid_for_loop())
    print("valid_function_call():")
    valid_function_call()