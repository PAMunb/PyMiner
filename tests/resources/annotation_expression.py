async def async_func_no_return_annotation(x: int):
    for i in range(x):
        print(i)
    return "done"

async def async_func_with_return_annotation(x: int) -> str:
    if x > 0:
        return "Positive"
    else:
        return "Negative"

def func_with_return_annotation(a: int, b: int) -> float:
    result = a / b
    return result

def func_no_return_annotation(a: int, b: int):
    result = a * b
    return result

def no_return_no_annotation():
    print("This function does nothing")

class ExampleClass:
    def method_with_annotation(self, name: str) -> str:
        return f"Hello, {name}!"

    async def async_method_with_annotation(self, n: int) -> bool:
        while n > 0:
            n -= 1
        return n == 0