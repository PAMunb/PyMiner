# Arquivo de teste com exemplos de Structural Pattern Matching

# Exemplo de 'structural_pattern_match'
def test_structural_pattern_match(value):
    match value:
        case 1:
            print("Número 1")  # Exemplo básico de correspondência de valor

# Exemplo de 'pattern_as'
def test_pattern_as(value):
    match value:
        case x as var:
            print(f"O valor {var} correspondeu ao padrão 'as'")

# Exemplo de 'pattern_or'
def test_pattern_or(value):
    match value:
        case 1 | 2 | 3:
            print("Corresponde a 1, 2 ou 3")

# Exemplo de 'pattern_sequence'
def test_pattern_sequence(value):
    match value:
        case [a, b, c]:
            print(f"Sequência: {a}, {b}, {c}")

# Exemplo de 'pattern_mapping'
def test_pattern_mapping(value):
    match value:
        case {"chave1": v1, "chave2": v2}:
            print(f"Mapeamento: chave1 -> {v1}, chave2 -> {v2}")

# Exemplo de 'pattern_class'
class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

def test_pattern_class(value):
    match value:
        case Pessoa(nome="Alice", idade=30):
            print("Pessoa: Alice, 30 anos")

# Exemplo de 'pattern_value'
def test_pattern_value(value):
    constante = 42
    match value:
        case constante:
            print("Corresponde ao valor da constante 42")

# Exemplo de 'pattern_singleton'
def test_pattern_singleton(value):
    match value:
        case None:
            print("Corresponde ao valor None (singleton)")

# Exemplo de 'pattern_star'
def test_pattern_star(value):
    match value:
        case [a, *rest]:
            print(f"Primeiro elemento: {a}, restantes: {rest}")
            
def match_star_pattern(seq):
    match seq:
        case [first, *middle, last]:
            print(f"Primeiro: {first}, Último: {last}, Meio: {middle}")
        case _:
            print("Outro tipo de sequência")

# Chamando as funções de teste para verificar os padrões
test_structural_pattern_match(1)
test_pattern_as(10)
test_pattern_or(2)
test_pattern_sequence([1, 2, 3])
test_pattern_mapping({"chave1": "valor1", "chave2": "valor2"})
test_pattern_class(Pessoa("Alice", 30))
test_pattern_value(42)
test_pattern_singleton(None)
test_pattern_star([1, 2, 3, 4])
