# Código com várias anotações válidas (positivos)
x: int = 5
y: str
class Pessoa:
    idade: int
    nome: str = "João"
def process_data(data: list[str]) -> int:
    total: int = 0
    return total

# Caso com anotações sem valor inicial
w: float
z: dict

# Código sem anotações da PEP 526
x = 5
y = "Python"

class Funcionario:
    idade = 30
    nome = "João"
    
    def process_data(data):
        total = 0
        return total

# Código com atribuições erradas que não são anotações da PEP 526
x = 5  # type: int
y = "Python"  # type: str

# Caso misto, com e sem anotações da PEP 526
x: int = 5
y = "Python"
class Pessoa:
    idade: int
    nome = "João"
    
    def process_data(data: list[str]) -> int:
        total = 0
        return total