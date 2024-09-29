# Importando o módulo typing
from typing import List, Dict, Tuple, Set, Optional, Union, Any, Callable, Iterable, TypeVar, Protocol

# 1. int, float, str, bool
def soma(a: int, b: int) -> int:
    return a + b

def dividir(x: float, y: float) -> float:
    return x / y

def cumprimentar(nome: str) -> str:
    return f"Olá, {nome}!"

def is_maior_de_idade(idade: int) -> bool:
    return idade >= 18

# 2. List
def somar_lista(numeros: List[int]) -> int:
    return sum(numeros)

# 3. Dict
def obter_preco(produtos: Dict[str, float], produto: str) -> Optional[float]:
    return produtos.get(produto)

# 4. Tuple
def coordenadas() -> Tuple[float, float]:
    return (10.5, 20.5)

# 5. Set
def verificar_numero_conjunto(numeros: Set[int], valor: int) -> bool:
    return valor in numeros

# 6. Optional
def saudacao(nome: Optional[str] = None) -> str:
    if nome:
        return f"Olá, {nome}!"
    return "Olá, visitante!"

# 7. Union
def processar_valor(valor: Union[int, float]) -> float:
    return valor * 2.5

# 8. Any
def imprimir_dado(dado: Any) -> None:
    print(dado)

# 9. Callable
def executar_funcao(funcao: Callable[[int, int], int], a: int, b: int) -> int:
    return funcao(a, b)

# 10. Iterable
def listar_numeros(numeros: Iterable[int]) -> None:
    for numero in numeros:
        print(numero)

# 11. TypeVar
T = TypeVar('T')

def devolver_mesmo_valor(valor: T) -> T:
    return valor

# 12. Protocol (Python 3.8+)
class Comparavel(Protocol):
    def comparar(self, outro: 'Comparavel') -> bool:
        pass

class Produto:
    def _init_(self, preco: float):
        self.preco = preco

    def comparar(self, outro: 'Produto') -> bool:
        return self.preco < outro.preco

# Exemplo de uso
if _name_ == "_main_":
    # 1. Usando int, float, str, bool
    print(soma(5, 3))
    print(dividir(10.0, 2.0))
    print(cumprimentar("Lucas"))
    print(is_maior_de_idade(20))

    # 2. Usando List
    print(somar_lista([1, 2, 3, 4, 5]))

    # 3. Usando Dict
    produtos = {"banana": 2.50, "maçã": 3.00}
    print(obter_preco(produtos, "banana"))

    # 4. Usando Tuple
    print(coordenadas())

    # 5. Usando Set
    conjunto = {1, 2, 3, 4}
    print(verificar_numero_conjunto(conjunto, 3))

    # 6. Usando Optional
    print(saudacao())
    print(saudacao("Walter"))

    # 7. Usando Union
    print(processar_valor(10))
    print(processar_valor(10.5))

    # 8. Usando Any
    imprimir_dado("Texto")
    imprimir_dado(100)

    # 9. Usando Callable
    def somar(a: int, b: int) -> int:
        return a + b

    print(executar_funcao(somar, 5, 7))

    # 10. Usando Iterable
    listar_numeros([10, 20, 30])

    # 11. Usando TypeVar
    print(devolver_mesmo_valor(100))
    print(devolver_mesmo_valor("Texto"))

    # 12. Usando Protocol
    p1 = Produto(50.0)
    p2 = Produto(30.0)
    print(p1.comparar(p2))