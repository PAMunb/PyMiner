def no_type_hints():
    pass

def single_type_hint(a: int) -> None:
    pass

class Example:
    x: int
    y: str = "hello"

def func(a: int, b: str) -> None:
    pass

class NoAnnotations:
    def method(self):
        pass