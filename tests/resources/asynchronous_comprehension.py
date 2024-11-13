import asyncio

# Função geradora assíncrona que simula uma operação de I/O
async def async_gen():
    for i in range(5):
        await asyncio.sleep(0.1)  # Simula uma operação assíncrona
        yield i

# Função que utiliza compreensão assíncrona para criar uma lista
async def async_list_comprehension():
    result = [i async for i in async_gen()]
    print("Resultado da lista com compreensão assíncrona:", result)

# Função que utiliza compreensão assíncrona para criar um conjunto
async def async_set_comprehension():
    result = {i async for i in async_gen() if i % 2 == 0}  # Apenas números pares
    print("Resultado do conjunto com compreensão assíncrona:", result)

# Função que utiliza compreensão assíncrona para criar um dicionário
async def async_dict_comprehension():
    result = {i: i ** 2 async for i in async_gen()}  # Mapeia i para i ao quadrado
    print("Resultado do dicionário com compreensão assíncrona:", result)

# Função que utiliza expressão geradora assíncrona
async def async_generator_expression():
    gen_expr = (i ** 2 async for i in async_gen())
    async for value in gen_expr:
        print("Valor da expressão geradora assíncrona:", value)

# Função com async with e operações assíncronas
class AsyncContextManager:
    async def __aenter__(self):
        print("Entrando no contexto assíncrono")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        print("Saindo do contexto assíncrono")

async def async_with_example():
    async with AsyncContextManager() as manager:
        print("Dentro do contexto assíncrono")

# Função principal que chama todas as funções acima
async def main():
    await async_list_comprehension()
    await async_set_comprehension()
    await async_dict_comprehension()
    await async_generator_expression()
    await async_with_example()

# Executa o código assíncrono
if __name__ == "__main__":
    asyncio.run(main())
