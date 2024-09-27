from typing import TypeVar
from typing import TypeAlias

T = TypeVar('T')
def func(x: T) -> T:
    return x

#code_negative_typevar
def func(x) -> None:
    pass

#test_type_params_in_class
class MyClass:
    def __init__(self, value: T) -> None:
        self.value = value

       
#test_type_params_in_function
    def func(x: T) -> T:
            pass
        
#test_incorrect_type_var_usage
x = TypeVar('T')


MyList: TypeAlias = list[str]