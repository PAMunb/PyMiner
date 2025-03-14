# arquivo: test_functions_annotations.py

# 1) Função sem nenhuma anotação
def foo_no_annotation(a, b):
    return a + b

# 2) Função com anotação em parâmetros, mas sem anotação de retorno
def bar_with_param_annotation(a: int, b: float):
    return a + b

# 3) Função com anotação em parâmetros e anotação de retorno
def baz_with_full_annotation(a: str) -> bool:
    return a == "yes"

# 4) Função com anotação de retorno, mas sem anotações em parâmetros
def qux_return_annotation_only(a, b) -> int:
    return a * b

# 5) Função assíncrona (async) com anotação em parâmetros
async def async_func_with_param(x: int):
    return x + 1

# 6) Função assíncrona com anotação de retorno
async def async_func_with_return(y) -> str:
    return f"Value = {y}"

# 7) Função sem parâmetros, mas com anotação de retorno
def no_args_but_annotated_return() -> None:
    print("Hello from a no-args function!")
    return

# 8) Função com função aninhada (outer_func anotada, inner_func sem anotações)
def outer_func(x: int) -> int:
    def inner_func(y):
        # Sem anotações
        return y + 1

    return inner_func(x)


# 7) Função sem parâmetros, mas com anotação de retorno
def async_with_full_annotation(y: int) -> None:
    print(f"Hello from a full annotation {y} function!")
    return