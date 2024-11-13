# Exemplo de função corrotina (async def)
async def fetch_data():
    await fetch_from_database()
    await process_data()

# Exemplo de uso de async for
async def async_for_example():
    async for item in fetch_items():
        print(item)

# Exemplo de uso de async with
async def async_with_example():
    async with acquire_connection() as conn:
        await conn.send_data("Hello")

# Função corrotina com várias estruturas assíncronas
async def complex_coroutine():
    await process_data()
    
    async with some_async_context():
        await another_awaitable()
        
    async for item in another_async_generator():
        await handle_item(item)

# Exemplo de função síncrona com await (não permitido, apenas para referência)
# def invalid_function():
    # Isso não funcionaria sem async def
    # await some_function()

# Função corrotina que retorna um awaitable
async def return_awaitable():
    return fetch_data()  # Retorna uma corrotina

# Exemplo de await com chamadas encadeadas
async def await_chained_calls():
    result = await fetch_data().process().finalize()

# Exemplo de await dentro de uma expressão condicional
async def conditional_await(flag):
    if flag:
        await fetch_data()
    else:
        await process_data()

# Exemplo adicional de async for com lógica interna
async def async_for_with_logic():
    async for item in generate_async_items():
        if item > 5:
            await handle_large_item(item)


#Em Python, uma expressão await não precisa obrigatoriamente envolver uma chamada de função (ast.Call). Qualquer objeto que seja "awaitable" — isto é, que implemente o protocolo de espera — pode ser usado com await. Aqui estão alguns exemplos de expressões await que não envolvem ast.Call:

async def fetch_data():
    return "data"

async def main():
    coro = fetch_data()  # Corrotina é criada, mas ainda não é chamada
    await coro  # Aguarda diretamente o objeto corrotina


async def generator_example():
    yield 10

async def main2():
    gen = generator_example()
    await gen
    
class CustomAwaitable:
    def __await__(self):
        yield 42  # Este valor é yield apenas para simular uma espera

async def main3():
    custom_obj = CustomAwaitable()
    await custom_obj  # Await no objeto personalizado
    
import asyncio

async def delayed_result():
    await asyncio.sleep(1)
    return "Resultado"

async def main4():
    pending_task = delayed_result()  # Corrotina criada
    await pending_task  # Aguarda o objeto corrotina diretamente
