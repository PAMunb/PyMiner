# Teste positivo 1: Contém um gerador assíncrono e um laço async for
import asyncio
    
async def gerador_assincrono():
    for i in range(3):
        await asyncio.sleep(1)
        yield i
    
async def main():
    async for valor in gerador_assincrono():
        print(valor)
        
# Teste positivo 2: Contém dois geradores assíncronos
    
async def gerador1():
    yield 1
    
async def gerador2():
    yield 2
    

# Teste negativo 1: Função assíncrona, mas não é gerador (sem yield)
async def funcao_assincrona():
   await asyncio.sleep(1)

# Teste negativo 2: Laço for comum, mas não async for
def funcao_sincrona():
        for i in range(3):
            print(i)

#teste negativo 3: Código sem programação assíncrona
def funcao_comum():
        return 42



import aiohttp
import asyncio

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def async_generator(urls):
    async with aiohttp.ClientSession() as session:
        for url in urls:
            yield await fetch_url(session, url)

async def main():
    urls = ["https://example.com", "https://example.org"]
    async for content in async_generator(urls):
        print(content)

asyncio.run(main())


import asyncio

async def count_down(n):
    while n > 0:
        await asyncio.sleep(1)
        yield n
        n -= 1

async def main():
    async for number in count_down(5):
        print(number)

asyncio.run(main())


import asyncio

# Um gerador assíncrono simples
async def async_generator():
    for i in range(5):
        await asyncio.sleep(1)  # Simula uma operação assíncrona
        yield i

# Consumindo o gerador assíncrono
async def main():
    async for value in async_generator():
        print(value)

# Executando a função principal
asyncio.run(main())
