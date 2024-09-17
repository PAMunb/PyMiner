import asyncio


async def my_coroutine():
    await asyncio.sleep(1)
    # await asyncio.sleep(1)  # Comentário, não deve ser contado
    string = "await asyncio.sleep(1)"  # String, não deve ser contado
    return 42

async def another_coroutine():
    result = await my_coroutine()
    return result


def regular_function():
    a = 0
    #await asyncio.sleep(1)