#test_multiple_functions
def func(a, b, *, c, d):
    pass

def another_func(x, y, z, *, w, v):
    pass
   
#test_no_keyword_only_args
def func(a, b, c):
    pass

#test_mixed_args
def func(a, b, *args, c, d):
    pass

def another_func(x, y, *args, z, *, w, v):
    pass


#test_keyword_only_args_in_class(self):
class MyClass:
    def method(self, a, b, *, c, d):
        pass
       
#test_no_functions
        
x = 10
y = 20
