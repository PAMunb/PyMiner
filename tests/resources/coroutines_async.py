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