#test_no_unpacking
a, b, c = [1, 2, 3]

#test_single_unpacking
a, *b = [1, 2, 3, 4, 5]

#test_multiple_unpacking
a, *b, c = [1, 2, 3, 4, 5]
d, *e = [6, 7, 8, 9]

#test_unpacking_in_function
def func(*args):
    a, *b = args
    
#test_nested_unpacking    
a, (b, *c), d = (1, (2, 3, 4), 5)

#test_unpacking_with_defaults
def func(a, *args, b=2):
    *rest, last = [1, 2, 3, 4]