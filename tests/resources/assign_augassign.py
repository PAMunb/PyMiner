# arquivo: test_cases.py

# 1) AnnAssign (variável anotada, PEP 526) com valor
x: int = 10

# 2) AnnAssign sem valor (ainda conta como AnnAssign)
y: str

# 3) Assign simples sem comentário de tipo
z = 30

# 4) Assign múltiplo sem comentário de tipo
a, b = 1, 2

# 5) Assign com comentário de tipo (Python 3.8+)
c = 50  # type: float

# 6) AugAssign
d = 5
d += 3
d *= 2

# Mais alguns exemplos em função
def foo():
    # AnnAssign dentro de função
    e: bool = True
    
    # Assign simples
    f = 'hello'
    
    # AugAssign
    f += ' world'
    
    # Assign com comentário de tipo
    g = 3  # type: int
    
    return f

# Fim do arquivo de teste