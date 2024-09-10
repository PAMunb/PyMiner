import asyncio

# Função utilizando o padrão match-case
def process_value(value):
    match value:
        case 'string':
            print("É uma string")
        case 42:
            print("É o número 42")
        case _:
            print("Outro valor")

# Função assíncrona com match-case
async def async_process(value):
    match value:
        case 'async':
            await asyncio.sleep(1)
            return "Async string"
        case _:
            return "Async default"

# Função sem o padrão match-case para comparação
def process_value_without_match(value):
    if value == 'string':
        print("É uma string")
    elif value == 42:
        print("É o número 42")
    else:
        print("Outro valor que não é match.")

# Função assíncrona sem match-case para comparação
async def async_process_without_match(value):
    if value == 'async':
        await asyncio.sleep(1)
        return "Async string"
    else:
        return "Async default"

def literal_match(value):
    match value:
        case 1:
            print("É o número 1")
        case 'hello':
            print("É a string 'hello'")
        case True:
            print("É o valor booleano True")
            
def match_singleton(value):
    match value:
        case None:  # Singleton None
            print("O valor é None")
        case True:  # Singleton True
            print("O valor é True")
        case False:  # Singleton False
            print("O valor é False")
        case _:
            print("Outro valor")
            
            
def match_with_guard(value):
    match value:
        case x if x > 10:
            print(f"O valor {x} é maior que 10")
        case x if x < 10:
            print(f"O valor {x} é menor que 10")
        case _:
            print("O valor é 10")
            
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def match_class_instance(point):
    match point:
        case Point(x, y):
            print(f"Point com x={x}, y={y}")
        case _:
            print("Não é um ponto")
            
            
def sequence_match(seq):
    match seq:
        case [x, y, z]:  # Lista ou tupla com exatamente 3 elementos
            print(f"Três elementos: {x}, {y}, {z}")
        case [x, y]:  # Lista ou tupla com exatamente 2 elementos
            print(f"Dois elementos: {x}, {y}")
        case []:
            print("Lista vazia")
        case _:
            print("Outro tipo de sequência")
            
def match_dict(d):
    match d:
        case {'nome': nome, 'idade': idade}:  # Deconstrói dicionário com as chaves 'nome' e 'idade'
            print(f"Nome: {nome}, Idade: {idade}")
        case {'nome': nome}:
            print(f"Nome: {nome}, idade desconhecida")
        case _:
            print("Não é um dicionário correspondente")
            
            
def match_or_pattern(value):
    match value:
        case 'apple' | 'banana':  # Corresponde a 'apple' ou 'banana'
            print("É uma fruta")
        case 42 | 100:
            print("É um número especial")
        case _:
            print("Outro valor")
            
def match_with_capture(value): #match_as
    match value:
        case [x, y] as coordenadas:  # Captura o valor correspondente
            print(f"Coordenadas: {coordenadas} com x={x}, y={y}")
        case _:
            print("Outro valor")
            
def match_nested_structure(data):
    match data:
        case {'point': {'x': x, 'y': y}}:
            print(f"Point dentro de um dicionário: x={x}, y={y}")
        case _:
            print("Outro tipo de estrutura")
            
def wildcard_match(value):
    match value:
        case [x, _, z]:  # Ignora o segundo elemento
            print(f"O primeiro e o terceiro elementos são {x} e {z}")
        case _:
            print("Outro valor")
            
from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

def match_enum(color):
    match color:
        case Color.RED:
            print("A cor é vermelha")
        case Color.GREEN:
            print("A cor é verde")
        case Color.BLUE:
            print("A cor é azul")
        case _:
            print("Cor desconhecida")
            
            
def match_exception(err):
    match err:
        case ValueError():
            print("Erro de valor!")
        case KeyError():
            print("Erro de chave!")
        case _:
            print("Outro tipo de erro")
            
            
def match_star_pattern(seq):
    match seq:
        case [first, *middle, last]:
            print(f"Primeiro: {first}, Último: {last}, Meio: {middle}")
        case _:
            print("Outro tipo de sequência")

# Testes simples para verificar as funções
def run_tests():
    process_value('string')          # Deve imprimir "É uma string"
    process_value(42)                # Deve imprimir "É o número 42"
    process_value('something else')  # Deve imprimir "Outro valor"

    asyncio.run(async_process('async'))         # Deve retornar "Async string" após aguardar 1 segundo
    asyncio.run(async_process('another value')) # Deve retornar "Async default"

    # Testando funções sem match-case
    process_value_without_match('string')         # Deve imprimir "É uma string"
    process_value_without_match(42)               # Deve imprimir "É o número 42"
    process_value_without_match('something else') # Deve imprimir "Outro valor"

    asyncio.run(async_process_without_match('async'))         # Deve retornar "Async string" após aguardar 1 segundo
    asyncio.run(async_process_without_match('another value')) # Deve retornar "Async default"

if __name__ == "__main__":
    run_tests()
