
def test_multiple():
    x = 10
    def inner1():
        nonlocal x
    def inner2():
        nonlocal x
        x += 1
        
def test_no_nonlocal():
    x = 10
    
    def inner():
        x += 1


def test_nonlocal_in_nested_functions():
    x = 10
    def inner1():
        nonlocal x
    def inner2():
        def inner3():
            nonlocal x           


def test_nonlocal_with_other_scopes():
    x = 10
    def inner1():
        nonlocal x
    def inner2():
        def inner3():
            nonlocal x
    def inner4():
        y = 20
        def inner5():
            nonlocal y

