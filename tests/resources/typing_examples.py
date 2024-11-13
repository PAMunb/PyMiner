from typing import List, Dict, Tuple, Set, FrozenSet, Type, Union, Optional, Deque, DefaultDict, OrderedDict, Counter, ChainMap, Callable

# Exemplos com typing

# List, Dict, Tuple, Set, FrozenSet, Type, Union, Optional
lista: List[int] = [1, 2, 3]                      # Lista de inteiros
dicionario: Dict[str, int] = {"um": 1, "dois": 2} # Dicionário de strings e inteiros
tupla: Tuple[int, str] = (10, "dez")              # Tupla de inteiro e string
conjunto: Set[int] = {1, 2, 3}                    # Conjunto de inteiros
conjunto_imutavel: FrozenSet[str] = frozenset(["a", "b"])  # Conjunto imutável de strings
tipo_objeto: Type[int] = int                      # Representação do tipo inteiro
opcional: Optional[str] = None                    # Tipo opcional (pode ser 'str' ou 'None')

# Union, Callable
valor: Union[int, str] = "Texto"                  # Pode ser int ou str
def executar(funcao: Callable[[int], int], valor: int) -> int:
    return funcao(valor)

# Deque, DefaultDict, OrderedDict, Counter, ChainMap
fila: Deque[int] = Deque([1, 2, 3])              # Deque de inteiros
contagem: DefaultDict[str, int] = DefaultDict(int) # DefaultDict com strings e inteiros
ordenado: OrderedDict[str, int] = OrderedDict()  # OrderedDict de strings e inteiros
contador: Counter[str] = Counter("exemplo")      # Counter de caracteres em uma string
mapa: ChainMap = ChainMap({'a': 1}, {'b': 2})    # ChainMap de dicionários

# Exemplos de anotações mais complexas
Matriz = List[List[int]]                          # Matriz de inteiros