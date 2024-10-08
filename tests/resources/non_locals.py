
def test_multiple():
    x = 10
    def inner1():
        nonlocal x
    def inner2():
        nonlocal x
        x += 1
        
def test_no_nonlocal():
<<<<<<< HEAD
    xw = 10
=======
    xw = 10
    
>>>>>>> def3526823cb4723c4792c3afb540180796c0bb8
    def inner():
        xw += 1


def test_nonlocal_in_nested_functions():
    xy = 10
    def inner1():
        nonlocal xy
    def inner2():
        def inner3():
            nonlocal xy          


def test_nonlocal_with_other_scopes():
    xv = 10
    def inner1():
        nonlocal xv
    def inner2():
        def inner3():
            nonlocal xv
    def inner4():
        yv = 20
        def inner5():
            nonlocal yv

