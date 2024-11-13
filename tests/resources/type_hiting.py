
# Exemplos de Type Hinting de acordo com a PEP 585

from ast import Match
from collections import deque, defaultdict, OrderedDict, Counter, ChainMap
from collections.abc import Awaitable, Coroutine, AsyncIterable, AsyncIterator, AsyncGenerator, Hashable, Iterable, Iterator, Generator, Reversible, Container, Collection, Callable, Set, MutableSet, Mapping, MutableMapping, Sequence, MutableSequence, ByteString, MappingView, KeysView, ItemsView, ValuesView
import re
from contextlib import AbstractContextManager, AbstractAsyncContextManager

# Variáveis globais com anotações de tipo
x: int = 42                          # Inteiro
y: float = 3.14                      # Float
nome: str = "Walter"                 # String
itens: list[str] = ["item1", "item2"]  # Lista de strings
config: dict[str, str] = {"key": "value"}  # Dicionário com chaves e valores de string
conjunto: set[int] = {1, 2, 3} # Conjunto de inteiros
tupla: tuple[float, float] = (y, y) # exemplo de tupla
conjuntos_imutaveis: frozenset[int] = frozenset([1, 2, 3, 4, 5])  # Frozenset de inteiros
tipo_dados: type = str  # Anotação de tipo que representa o tipo 'str'

# Variáveis globais sem anotações de tipo
mensagem = "Olá, mundo!"             # String
contagem = 100                        # Inteiro
ativo = True                          # Booleano
elementos = []                        # Lista vazia

class MinhaClasse:
    items: list[str]  # Anotação de tipo para um atributo da classe
    occurrences: dict[str, int]  # Outro exemplo de anotação de tipo

class Armazenamento:
    def __init__(self):
        self.itens: list[str] = []  # Lista de itens do tipo string
        self.ocorrencias: dict[str, int] = {}  # Dicionário com chaves do tipo string e valores do tipo inteiro

    def adicionar_item(self, item: str) -> None:
        self.itens.append(item)
        if item in self.ocorrencias:
            self.ocorrencias[item] += 1
        else:
            self.ocorrencias[item] = 1

class Grupo:
    def __init__(self):
        self.membros: set[str] = set()  # Conjunto de membros do tipo string

    def adicionar_membro(self, membro: str) -> None:
        self.membros.add(membro)

    def tem_membro(self, membro: str) -> bool:
        return membro in self.membros

class Coordenadas:
    def __init__(self, latitude: float, longitude: float):
        self.localizacao: tuple[float, float] = (latitude, longitude)  # Tupla para coordenadas

    def obter_coordenadas(self) -> tuple[float, float]:
        return self.localizacao
    
class Catalogo:
    def __init__(self):
        self.itens: frozenset[str] = frozenset()  # Conjunto imutável de itens do tipo string

    def adicionar_item(self, item: str) -> None:
        # Como frozenset é imutável, criar uma nova instância ao adicionar
        self.itens = self.itens.union({item})

    def obter_itens(self) -> frozenset[str]:
        return self.itens
    
class TipoObjeto:
    def __init__(self, objeto: object):
        self.tipo: type = type(objeto)  # Tipo do objeto passado

    def obter_tipo(self) -> str:
        return self.tipo.__name__  # Retorna o nome do tipo
    
    def outer_function(param: int) -> None:
        def inner_function(inner_param: str) -> None:
            pass

# 1. tuple
def processar_dados(dados: tuple[int, str]) -> None:
    print(f"Id: {dados[0]}, Nome: {dados[1]}")

# 2. list
def somar_lista(valores: list[int]) -> int:
    return sum(valores)

# 3. dict
def contar_ocorrencias(texto: str) -> dict[str, int]:
    palavras = texto.split()
    return {palavra: palavras.count(palavra) for palavra in set(palavras)}

# 4. set
def adicionar_elementos(conjunto: set[int], elementos: list[int]) -> set[int]:
    for elemento in elementos:
        conjunto.add(elemento)
    return conjunto

# 5. frozenset
def criar_frozenset(valores: list[int]) -> frozenset[int]:
    return frozenset(valores)

# 6. type
def obter_tipo(objeto: object) -> type:
    return type(objeto)


# 7. collections.deque
def manipular_deque(entrada: deque[int]) -> None:
    entrada.append(4)
    entrada.appendleft(1)

# 8. collections.defaultdict
def contar_ocorrencias_defaultdict(texto: str) -> defaultdict[str, int]:
    contagem = defaultdict(int)
    for palavra in texto.split():
        contagem[palavra] += 1
    return contagem

# 9. collections.OrderedDict
def ordenar_dict(d: dict[str, int]) -> OrderedDict[str, int]:
    return OrderedDict(sorted(d.items(), key=lambda item: item[1]))

# 10. collections.Counter
def contar_caracteres(texto: str) -> Counter[str]:
    return Counter(texto)

# 11. collections.ChainMap
def combinar_mapas(mapa1: dict[str, int], mapa2: dict[str, int]) -> ChainMap[str, int]:
    return ChainMap(mapa1, mapa2)

# 12. collections.abc.Awaitable
async def esperar_por_entrada(entrada: Awaitable[str]) -> str:
    return await entrada

# 13. collections.abc.Coroutine
async def exemplo_coroutine() -> Coroutine:
    return await asyncio.sleep(1, result="Resultado")

# 14. collections.abc.AsyncIterable
async def iterar_async(iteravel: AsyncIterable[int]) -> None:
    async for valor in iteravel:
        print(valor)

# 15. collections.abc.AsyncIterator
class MeuAsyncIterator(AsyncIterator[int]):
    async def __anext__(self) -> int:
        # Lógica para retornar o próximo item
        pass

# 16. collections.abc.AsyncGenerator
async def gerar_async() -> AsyncGenerator[int, None]:
    for i in range(5):
        yield i

# 17. collections.abc.Iterable
def processar_iteravel(entrada: Iterable[str]) -> list[str]:
    return [item.upper() for item in entrada]

# 18. collections.abc.Iterator
def obter_iterador(entrada: list[int]) -> Iterator[int]:
    return iter(entrada)

# 19. collections.abc.Generator
def gerar_numeros() -> Generator[int, None, None]:
    for i in range(5):
        yield i

# 20. collections.abc.Reversible
def reversivel(entrada: Reversible[int]) -> list[int]:
    return list(reversed(entrada))

# 21. collections.abc.Container
def contem_elemento(container: Container[int], elemento: int) -> bool:
    return elemento in container

# 22. collections.abc.Collection
def tamanho_colecao(colecao: Collection[int]) -> int:
    return len(colecao)

# 23. collections.abc.Callable
def executar(func: Callable[[int], int], valor: int) -> int:
    return func(valor)

# 24. collections.abc.Set
def somar_conjunto(conjunto: Set[int]) -> int:
    return sum(conjunto)

# 25. collections.abc.MutableSet
def adicionar_elemento(mutable_set: MutableSet[int], elemento: int) -> None:
    mutable_set.add(elemento)

# 26. collections.abc.Mapping
def obter_valor(mapa: Mapping[str, int], chave: str) -> int:
    return mapa.get(chave, 0)

# 27. collections.abc.MutableMapping
def atualizar_mapping(mapping: MutableMapping[str, int], chave: str, valor: int) -> None:
    mapping[chave] = valor

# 28. collections.abc.Sequence
def acessar_elemento(sequencia: Sequence[int], indice: int) -> int:
    return sequencia[indice]

# 29. collections.abc.MutableSequence
def adicionar_elemento_mutavel(sequencia: MutableSequence[int], elemento: int) -> None:
    sequencia.append(elemento)

# 30. collections.abc.ByteString
def processar_bytes(dados: ByteString) -> str:
    return dados.decode()

# 31. collections.abc.MappingView
def obter_keys(mapping_view: MappingView[str, int]) -> list[str]:
    return list(mapping_view)

# 32. collections.abc.KeysView
def exibir_chaves(keys_view: KeysView[str]) -> None:
    for chave in keys_view:
        print(chave)

# 33. collections.abc.ItemsView
def exibir_items(items_view: ItemsView[str, int]) -> None:
    for chave, valor in items_view:
        print(f"{chave}: {valor}")

# 34. collections.abc.ValuesView
def exibir_valores(values_view: ValuesView[int]) -> None:
    for valor in values_view:
        print(valor)

# 35. contextlib.AbstractContextManager
class MeuContexto(AbstractContextManager):
    def __enter__(self):
        print("Iniciando contexto")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Saindo do contexto")

# 36. contextlib.AbstractAsyncContextManager
class MeuAsyncContexto(AbstractAsyncContextManager):
    async def __aenter__(self):
        print("Iniciando contexto assíncrono")
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        print("Saindo do contexto assíncrono")

# 37. re.Pattern
def encontrar_padrao(padrao: re.Pattern, texto: str) -> bool:
    return bool(padrao.search(texto))

# 38. re.Match
def obter_match(padrao: re.Pattern, texto: str) -> re.Match | None:
    return padrao.match(texto)

async def minha_coroutine() -> Coroutine:
    await asyncio.sleep(1)
    return "Resultado da Coroutine"

# Para executar a coroutine
asyncio.run(minha_coroutine())

def processar_bytes(dados: ByteString) -> str:
    return dados.decode('utf-8')

# Uso
resultado = processar_bytes(b"Exemplo de Bytes")
print(resultado)  # Saída: Exemplo de Bytes

class MeuContexto(AbstractContextManager):
    def __enter__(self):
        print("Iniciando contexto")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Saindo do contexto")

# Uso
with MeuContexto() as contexto:
    print("Dentro do contexto")
    
from contextlib import AbstractAsyncContextManager
import asyncio

class MeuAsyncContexto(AbstractAsyncContextManager):
    async def __aenter__(self):
        print("Iniciando contexto assíncrono")
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        print("Saindo do contexto assíncrono")

# Uso
async def main():
    async with MeuAsyncContexto():
        print("Dentro do contexto assíncrono")

# Executar a função assíncrona
asyncio.run(main())

def encontrar_padrao(padrao: re.Pattern, texto: str) -> bool:
    return bool(padrao.search(texto))

# Uso
padrao = re.compile(r'\d+')
resultado = encontrar_padrao(padrao, "O número é 123")
print(resultado)  # Saída: True

def obter_match(padrao: re.Pattern, texto: str) -> Match | None:
    return padrao.match(texto)

# Uso
padrao = re.compile(r'^[A-Z]')
match_resultado = obter_match(padrao, "Exemplo")
if match_resultado:
    print("Match encontrado:", match_resultado.group())
else:
    print("Nenhum match encontrado")
    
async def minha_coroutine() -> str:
    return "Resultado da Coroutine"

def test_minha_coroutine():
    import asyncio
    resultado = asyncio.run(minha_coroutine())
    assert resultado == "Resultado da Coroutine"
    
def obter_match(padrao, texto):
    return padrao.match(texto)

# Compila um padrão de expressão regular
padrao_exemplo = re.compile(r'^[A-Z][a-z]*')

# Testando a função
resultado = obter_match(padrao_exemplo, "Exemplo")
if resultado:
    print(f'Match encontrado: {resultado.group()}')
else:
    print('Nenhum match encontrado.')

# Outro teste que não deve encontrar um match
resultado = obter_match(padrao_exemplo, "exemplo")
if resultado:
    print(f'Match encontrado: {resultado.group()}')
else:
    print('Nenhum match encontrado.')