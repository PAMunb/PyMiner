type ListOrSet[T] = list[T] | set[T]

def func[T](a: T, b: T) -> T:
    return None

class ClassA[T: str]:
    def method1(self) -> T:
        return None
    
class ClassA[T: dict[str, int]]: ...  # OK

class ClassB[T: "ForwardReference"]: ...  # OK

class ClassA[AnyStr: (str, bytes)]: ...  # OK

class ClassB[T: ("ForwardReference", bytes)]: ...  # OK


# A type alias that includes a forward reference
type AnimalOrVegetable = Animal | "Vegetable"

# A generic self-referential type alias
type RecursiveList[T] = T | list[RecursiveList[T]]


# A non-generic type alias
type IntOrStr = int | str

# A generic type alias
type ListOrSet[T] = list[T] | set[T]


type IntFunc[**P] = Callable[P, int]  # ParamSpec
type LabeledTuple[*Ts] = tuple[str, *Ts]  # TypeVarTuple
type HashableSequence[T: Hashable] = Sequence[T]  # TypeVar with bound
type IntOrStrSequence[T: (int, str)] = Sequence[T]  # TypeVar with constraints


################# Sintaxe antiga para validação..

from typing import TypeVar

# TypeVar com 'bound' e 'constraints'
T1 = TypeVar('T1', bound=int)  # Somente int ou subtipos
T2 = TypeVar('T2', int, str)    # Somente int ou str

def process_int(item: T1) -> T1:
    return item

def process_item(item: T2) -> T2:
    return item

# Funciona: 42 é um int, que é o limite superior
print(process_int(42))   # OK

# Funciona: 'int' está nas restrições
print(process_item(42))   # OK

# Funciona: 'str' está nas restrições
print(process_item('hello'))  # OK

from typing import Generic, TypeVar

_T_co = TypeVar("_T_co", covariant=True, bound=str)

class ClassA(Generic[_T_co]):
    def method1(self) -> _T_co:
        return None
    
from typing import Callable, ParamSpec

P = ParamSpec('P')

def executar_funcao_int(func: Callable[P, int], *args: P.args, **kwargs: P.kwargs) -> int:
    return func(*args, **kwargs)

def somar(a: int, b: int) -> int:
    return a + b

resultado = executar_funcao_int(somar, 10, 20)
print(resultado)  # Saída: 30

def rotular_tupla(*valores: *Ts) -> tuple[str, *Ts]:
    return ("Rótulo", *valores)

tupla = rotular_tupla(1, 2, 3, "texto")
print(tupla)  # Saída: ('Rótulo', 1, 2, 3, 'texto')