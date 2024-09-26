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

