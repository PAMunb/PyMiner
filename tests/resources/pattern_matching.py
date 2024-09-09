def process_value(value):
    match value:
        case 'string':
            print("É uma string")
        case 42:
            print("É o número 42")
        case _:
            print("Outro valor")

async def async_process(value):
    match value:
        case 'async':
            await asyncio.sleep(1)
            return "Async string"
        case _:
            return "Async default"