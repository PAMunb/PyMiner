# Código com uma compreensão assíncrona e um loop assíncrono
async def func():
    result = [x async for x in async_iter()]
    async for y in async_iter2():
        pass

# Código sem compreensões assíncronas e loops assíncronos
def func():
    result = [x for x in range(10)]


            