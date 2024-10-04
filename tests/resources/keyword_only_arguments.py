import asyncio

def funcao(a, b):
    return a + b

lista = [1, 2]
funcao(*lista)

#ele não computa como Starred.
async def funcao_variavel(*args):
    print(args)

asyncio.run(funcao_variavel(1, 2, 3))

#ele não computa como Starred.
def funcao_com_extensao(a, b, *args):
    print(a, b)  # Primeiros dois argumentos
    print(args)  # Todos os outros argumentos

funcao_com_extensao(1, 2, 3, 4, 5)  
# Saída:
# 1 2
# (3, 4, 5)

#ele não computa como Starred.
def funcao_completamente_extensa(a, *args, c):
    print(a)    # Primeiro argumento
    print(args) # Todos os argumentos após 'a'
    print(c)    # Último argumento nomeado

funcao_completamente_extensa(1, 2, 3, c=4)
# Saída:
# 1
# (2, 3)
# 4

# Exemplo 11: Desempacotamento em Funções Assíncronas
async def funcao_assincrona():
    valores = [1, 2, 3, 4, 5]
    primeiro, *restante = valores
    print(f"Primeiro: {primeiro}, Restante: {restante}")

# Exemplo 12: Usando async for com Desempacotamento
async def gerar_dados():
    for i in range(1, 4):
        await asyncio.sleep(1)  # Simula uma operação assíncrona
        yield (i, i * 2, i * 3)

async def usar_gerador():
    async for a, *b in gerar_dados():
        print(f"a: {a}, b: {b}")

# Exemplo 13: Usando async with com Desempacotamento
class AsyncContextManager:
    async def __aenter__(self):
        return (1, 2, 3)

    async def __aexit__(self, exc_type, exc_value, traceback):
        pass

async def usar_async_with():
    async with AsyncContextManager() as (x, *y):
        print(f"x: {x}, y: {y}")

# Função principal para executar os exemplos
async def main():
    await funcao_assincrona()
    await usar_gerador()
    await usar_async_with()

def main():
    print("=== Exemplo 1: Desempacotamento Básico ===")
    a, b, *resto = [1, 2, 3, 4, 5]
    print(f"a: {a}, b: {b}, resto: {resto}")
    
    print("\n=== Exemplo 2: Capturando Elementos no Início e no Fim ===")
    inicio, *meio, fim = [1, 2, 3, 4, 5]
    print(f"Inicio: {inicio}, Meio: {meio}, Fim: {fim}")

    print("\n=== Exemplo 3: Combinando com Outros Iteráveis ===")
    c, *d, e = (10, 20, 30, 40, 50)
    print(f"c: {c}, d: {d}, e: {e}")

    # Exemplo com conjunto
    f, *g = {100, 200, 300, 400}
    print(f"\nf: {f}, g: {g}")

    print("\n=== Exemplo 4: Atribuição em Funções ===")
    #ele não computa como Starred.
    def funcao(*args):
        print("Argumentos:", args)

    funcao(1, 2, 3)
    funcao('a', 'b', 'c', 'd')

    print("\n=== Exemplo 5: Combinando com Desempacotamento Regular ===")
    a, *b, c = [1, 2, 3, 4, 5]
    print(f"a: {a}, b: {b}, c: {c}")

    print("\n=== Exemplo 6: Desempacotamento de Dicionários ===")
    dicionario = {'a': 1, 'b': 2, 'c': 3}
    a, *b, c = dicionario
    print(f"a: {a}, b: {b}, c: {c}")

    print("\n=== Exemplo 7: Desempacotamento de Listas Aninhadas ===")
    listas = [[1, 2], [3, 4], [5, 6]]
    *primeiras, ultimo = listas
    print(f"primeiras: {primeiras}, ultimo: {ultimo}")

    print("\n=== Exemplo 8: Desempacotamento em um Loop ===")
    listas = [[1, 2], [3, 4], [5, 6]]
    for a, *b in listas:
        print(f"a: {a}, b: {b}")

    print("\n=== Exemplo 9: Desempacotamento em Estruturas de Dados Complexas ===")
    data = [(1, 'a'), (2, 'b'), (3, 'c')]
    for num, *letras in data:
        print(f"Numero: {num}, Letras: {letras}")

    print("\n=== Exemplo 10: Utilizando em um Loop com Intervalos ===")
    for x, *y in range(1, 10):
        print(f"x: {x}, y: {y}")

if __name__ == "__main__":
    main()


